# -*- coding: utf-8 -*-

from ecm.core.views.base import ContentCreateView


class WorkflowFolderCreateView(ContentCreateView):

    def get_exclude(self):
        return list(self.exclude) + ['state_initial', ]