# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView
from django.utils.translation import ugettext_lazy as _

from models import ECMRole, ECMPermission, ECMWorkflow


class RoleCreateView(CreateView):
    model = ECMRole
    template_name = "ecm/roles/create.html"

    def get_success_url(self):
        return reverse('roles_list')


class RoleListView(ListView):
    model = ECMRole
    template_name = "ecm/roles/list.html"

    def get_context_data(self, **kwargs):
        data = super(RoleListView, self).get_context_data(**kwargs)
        actions = [{'title': _("Create new role"),
                    'url': reverse('roles_create'),
                    'children': (),
                    }]
        extra = {'actions': actions, }
        data.update(extra)
        return data


class PermissionListView(ListView):
    model = ECMPermission
    template_name = "ecm/permissions/list.html"


class WorkflowCreateView(CreateView):
    model = ECMWorkflow
    template_name = "ecm/workflows/create.html"

    def get_success_url(self):
        return reverse('workflows_list')


class WorkflowListView(ListView):
    model = ECMWorkflow
    template_name = "ecm/workflows/list.html"

    def get_context_data(self, **kwargs):
        data = super(WorkflowListView, self).get_context_data(**kwargs)
        actions = [{'title': _("Create new worflow"),
                    'url': reverse('workflows_create'),
                    'children': (),
                    }]
        extra = {'actions': actions, }
        data.update(extra)
        return data
