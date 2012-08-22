# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from ecm.core import toc
from ecm.core.models import ECMBaseFolder
from ecm.security.models import ECMWorkflow


class ECMSite(ECMBaseFolder):
    """
    """
    allowed_content_types = ('ecmfolder', )
toc.register(ECMSite)


class ECMWorkflowFolder(ECMBaseFolder):
    """
    """
    create_view = "ecm.content.views.workflows.WorkflowFolderCreateView"
    allowed_content_types = ('ecmworkflow', )

    def get_children(self):
        return ECMWorkflow.objects.all()
toc.register(ECMWorkflowFolder)

class ECMFolder(ECMBaseFolder):
    """
    """

    class Meta:
        verbose_name = _("Folder")

    allowed_content_types = ('ecmfolder', )
toc.register(ECMFolder)

