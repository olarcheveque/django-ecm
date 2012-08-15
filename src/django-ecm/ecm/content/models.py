# -*- coding: utf-8 -*-

from ecm.core import toc
from ecm.core.models import ECMBaseFolder


class Folder(ECMBaseFolder):
    """
    """
    allowed_content_types = ('folder', )

toc.register(Folder)
