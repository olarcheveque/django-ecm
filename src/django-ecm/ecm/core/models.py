# -*- coding: utf-8 -*-

from django.db import models
from django.utils.decorators import classonlymethod

from django.contrib.contenttypes.models import ContentType

from uuidfield import UUIDField
from mptt.models import MPTTModel, TreeForeignKey
from uuslug import uuslug

from decorators import cached


class CatalogEntryManager(models.Manager):
    pass


class ECMEntryMixin:

    class Meta:
        abstract = True

    detail_view = "ecm.core.views.base.ContentDetailView"
    create_view = "ecm.core.views.base.ContentCreateView"
    update_view = "ecm.core.views.base.ContentUpdateView"

    id = UUIDField(auto=True, primary_key=True, unique=True)

    @property
    def class_verbose_name(self):
        return self._meta.verbose_name


class ECMCatalogEntry(MPTTModel, ECMEntryMixin):
    """
    """
    class Meta:
        db_table = "ecm_catalog"

    objects = CatalogEntryManager()

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=False, null=True)

    content_type = models.ForeignKey('contenttypes.ContentType')

    parent = TreeForeignKey('self', null=True, blank=True,
            related_name='+')

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, **kwargs):
        if self.slug is None:
            self.slug = uuslug(self.title, instance=self)

        if self.content_type_id is None:
            klass_name = self.__class__.__name__.lower()
            ct = ContentType.objects.get(model=klass_name)
            self.content_type = ct
        super(ECMCatalogEntry, self).save(**kwargs)

    def __unicode__(self):
        return u"[%s:%s] %s" % (self.content_type.model, self.id, self.title)

    def get_object(self):
        return self.content_type.get_object_for_this_type(id=self.id)

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


class ECMCatalog(ECMCatalogEntry):
    """
    Shortcut for CatalogEntry.
    """

    class Meta:
        proxy = True


class ECMPermissionMixin:
    default_permissions = [
            'view',
            'add',
            'edit',
            'delete',
            ]

    permissions = []

    @classonlymethod
    def get_permissions(cls):
        default = ["%s %s" % (p, cls.__name__) for p in
                cls.default_permissions]
        return default + list(cls.permissions)


class ECMBaseContent(ECMCatalogEntry, ECMPermissionMixin):
    """
    """
    class Meta:
        abstract = True


class ECMFolderMixin:
    allowed_content_types = ()


class ECMBaseFolder(ECMBaseContent, ECMFolderMixin):
    """
    """

    class Meta:
        abstract = True


class ECMStandaloneContent(models.Model, ECMPermissionMixin, ECMEntryMixin):

    class Meta:
        abstract = True

class ECMStandaloneFolder(ECMStandaloneContent, ECMFolderMixin):

    class Meta:
        abstract = True
