
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView
from django.utils.translation import ugettext_lazy as _

from ecm.core.models import ECMWorkflow


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
    

