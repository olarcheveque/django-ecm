# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.contenttypes.models import ContentType

from uuidfield import UUIDField
from mptt.models import MPTTModel, TreeForeignKey
from uuslug import uuslug

from mixins import ECMEntryMixin, ECMPermissionMixin, \
        ECMNavigationMixin,  ECMFolderMixin
from decorators import cached


class ECMCatalogEntry(MPTTModel, ECMEntryMixin, ECMNavigationMixin):
    """
    """
    class Meta:
        db_table = "ecm_catalog"

    id = UUIDField(auto=True, primary_key=True, unique=True)

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


class ECMBaseContent(ECMCatalogEntry, ECMPermissionMixin):
    """
    """
    class Meta:
        abstract = True


class ECMBaseFolder(ECMBaseContent, ECMFolderMixin):
    """
    """

    class Meta:
        abstract = True
