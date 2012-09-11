# -*- coding: utf-8 -*-

from ecm.core.views.base import ContentCreateView
from ecm.core.views.base import ContentFormsetView

from ecm.security.models import ECMPermission
from ecm.security.forms import ACLFormSet


class WorkflowCreateView(ContentCreateView):

    def get_exclude(self):
        return list(self.exclude) + ['state_initial', ]


class SetupPermissionView(ContentFormsetView):
    actions = ()
    form_class = ACLFormSet

    def get_initial(self):
        initial = [{'state': self.object, 'permission': p} \
                for p in ECMPermission.objects.all()]
        return initial

    def get_template_names(self):
        return ("ecm/ecmstate/setup_permissions.html", )
