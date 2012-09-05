# -*- coding: utf-8 -*-

from ecm.core.views.base import ContentCreateView
from ecm.core.views.base import ContentDetailView


class WorkflowCreateView(ContentCreateView):

    def get_exclude(self):
        return list(self.exclude) + ['state_initial', ]


class SetupPermissionView(ContentDetailView):
    actions = ()

    def get_template_names(self):
        return ("ecm/ecmstate/setup_permissions.html", )
