# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView
from django.utils.translation import ugettext_lazy as _

from ecm.core.models import ECMRole


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
    

