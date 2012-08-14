# -*- coding: utf-8 -*-

from ecm.core import toc
from ecm.core.models import BaseFolder


class Folder(BaseFolder):
    """
    """
    allowed_content_types = ('folder', )

toc.register(Folder)
