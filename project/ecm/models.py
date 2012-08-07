# -*- coding: utf-8 -*-

from django.db import models

from uuidfield import UUIDField
from mptt.models import MPTTModel, TreeForeignKey


class CatalogEntryManager(models.Manager):
    pass


class CatalogEntry(MPTTModel):
    """
    """

    class MPTTMeta:
        order_insertion_by = ['title']

    objects = CatalogEntryManager()

    uuid = UUIDField(auto=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    content_type = models.ForeignKey('contenttypes.ContentType')

    parent = TreeForeignKey('self', null=True, blank=True,
            related_name='children')

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"[%s:%s] %s" % (self.content_type.model, self.uuid, self.title)

    def get_object(self):
        return self.content_type.get_object_for_this_type(uuid=self.uuid)

    def get_absolute_path(self):
        segments = [a.slug for a in self.get_ancestors()]
        segments.append(self.slug)
        return "/".join(segments)

    @models.permalink
    def get_absolute_url(self):
        segments = [a.slug for a in self.get_ancestors()]
        url = '/'.join(segments)
        return ('content_detail', [url, self.slug])

    @models.permalink
    def get_absolute_edit_url(self):
        segments = [a.slug for a in self.get_ancestors()]
        url = '/'.join(segments)
        return ('content_edit', [url, self.slug])


class Catalog(CatalogEntry):
    """
    """

    class Meta:
        proxy = True


class Folder(CatalogEntry):
    description = models.CharField(max_length=50)


class Article(CatalogEntry):
    content = models.TextField(max_length=255)
