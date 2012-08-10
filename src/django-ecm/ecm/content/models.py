# -*- coding: utf-8 -*-

from django.db import models
from ecm.core.models import CatalogEntry

class Folder(CatalogEntry):
    """
    """
    detail_view = "ecm.content.views.FolderDetailView"

    description = models.CharField(max_length=50)


class Article(CatalogEntry):
    """
    """
    content = models.TextField(max_length=255)
