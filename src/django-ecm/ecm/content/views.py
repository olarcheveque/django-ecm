# -*- coding: utf-8 -*-

from ecm.core.views.base import ContentDetailView

class FolderDetailView(ContentDetailView):
    allowed_content_types = ('folder', 'article', )


