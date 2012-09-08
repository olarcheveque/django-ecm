# -*- coding: utf-8 -*-

from ecm.core.views.base import ContentCreateView
from ecm.core.views.base import ContentDetailView

from ecm.security.models import ECMPermission
from ecm.security.forms import ACLFormSet


class WorkflowCreateView(ContentCreateView):

    def get_exclude(self):
        return list(self.exclude) + ['state_initial', ]


class SetupPermissionView(ContentDetailView):
    actions = ()

    def get_template_names(self):
        return ("ecm/ecmstate/setup_permissions.html", )

    def get_context_data(self, **kwargs):
        data = super(SetupPermissionView, self).get_context_data(**kwargs)
        initial = [{'state': self.object, 'permission': p} \
                for p in ECMPermission.objects.all()]
        data['formset'] = ACLFormSet(initial=initial)
        return data
