# -*- coding: utf-8 -*-

import inspect
from django.db import models
from django.db.models import get_models
from django.db.models.signals import post_syncdb
from django.utils.decorators import classonlymethod

from django.contrib.contenttypes.models import ContentType

from uuidfield import UUIDField
from mptt.models import MPTTModel, TreeForeignKey
from decorators import cached


class ECMRole(models.Model):
    name = models.CharField(max_length=100)


class ECMPermission(models.Model):
    name = models.CharField(max_length=100)
    # for grouping purpose
    flag = models.CharField(max_length=100)


class CatalogEntryManager(models.Manager):
    pass


class CatalogEntry(MPTTModel):
    """
    """
    detail_view = "ecm.core.views.base.ContentDetailView"
    create_view = "ecm.core.views.base.ContentCreateView"
    update_view = "ecm.core.views.base.ContentUpdateView"

    class Meta:
        db_table = "ecm_catalog"


    class MPTTMeta:
        order_insertion_by = ['title']

    objects = CatalogEntryManager()

    uuid = UUIDField(auto=True, primary_key=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=False, null=True)

    content_type = models.ForeignKey('contenttypes.ContentType')

    parent = TreeForeignKey('self', null=True, blank=True,
            related_name='children')

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, **kwargs):
        if self.content_type_id is None:
            klass_name = self.__class__.__name__.lower()
            ct = ContentType.objects.get(model=klass_name)
            self.content_type = ct
        super(CatalogEntry, self).save(**kwargs)

    def __unicode__(self):
        return u"[%s:%s] %s" % (self.content_type.model, self.uuid, self.title)

    def get_object(self):
        return self.content_type.get_object_for_this_type(uuid=self.uuid)

    def get_traversal(self):
        traverse = list(self.get_ancestors()) + [self, ]
        return traverse

    def get_traversal_slugs(self):
        traverse = [a.slug for a in self.get_traversal()]
        return traverse

    @cached
    @models.permalink
    def get_absolute_url(self):
        slugs = self.get_traversal_slugs()
        url = "/".join(slugs)
        return ('content_detail', [url, ])

    @cached
    @models.permalink
    def get_absolute_edit_url(self):
        slugs = self.get_traversal_slugs()
        url = "/".join(slugs)
        return ('content_edit', [url, ])


class Catalog(CatalogEntry):
    """
    Shortcut for CatalogEntry.
    """

    class Meta:
        proxy = True


class BaseContent(CatalogEntry):
    """
    """
    default_permissions = [
            'view',
            'add',
            'edit',
            'delete',
            ]

    permissions = []

    class Meta:
        abstract = True

    @classonlymethod
    def get_permissions(cls):
        default = ["%s %s" % (p, cls.__name__) for p in
                cls.default_permissions]
        return default + list(cls.permissions)

class BaseFolder(BaseContent):
    """
    """
    allowed_content_types = ()
    class Meta:
        abstract = True

def create_ecm_permissions(app, created_models, verbosity, **kwargs):
    app_models = get_models(app)

    def traverse(data, search):
        if not hasattr(data, '__iter__'):
            if data == search:
                return True
            else:
                return False
        if hasattr(data, '__iter__'):
            found = False
            for kid in data:
                found = found | traverse(kid, search)
            return found

    for model in app_models:
        bases = inspect.getclasstree(inspect.getmro(model))
        if traverse(bases, BaseContent):
            flag = model.__name__
            for perm in model.get_permissions():
                p, created = ECMPermission.objects.get_or_create(
                        name=perm, flag=flag)
                if created:
                    print "permission '%s' created" % perm

post_syncdb.connect(create_ecm_permissions)
