# -*- coding: utf-8 -*-

from django.db import models

from uuidfield import UUIDField
from mptt.models import MPTTModel, TreeForeignKey

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

    def get_traversal(self):
        traverse = list(self.get_ancestors()) + [self, ]
        return traverse

    def get_traversal_slugs(self):
        traverse = [a.slug for a in self.get_traversal()]
        return traverse

    @models.permalink
    def get_absolute_url(self):
        slugs = self.get_traversal_slugs()
        url = "/".join(slugs)
        return ('content_detail', [url, ])

    @models.permalink
    def get_absolute_edit_url(self):
        slugs = self.get_traversal_slugs()
        url = "/".join(slugs)
        return ('content_edit', [url, ])


class Catalog(CatalogEntry):
    """
    """

    class Meta:
        proxy = True


class Folder(CatalogEntry):
    description = models.CharField(max_length=50)


class Article(CatalogEntry):
    content = models.TextField(max_length=255)
