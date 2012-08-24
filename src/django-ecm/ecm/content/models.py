# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from ecm.core import toc
from ecm.core.models import ECMBaseFolder

class ECMSite(ECMBaseFolder):
    """
    """
    allowed_content_types = ('ecmfolder', )
toc.register(ECMSite)


class ECMFolder(ECMBaseFolder):
    """
    """

    class Meta:
        verbose_name = _("Folder")

    allowed_content_types = ('ecmfolder', )
toc.register(ECMFolder)

