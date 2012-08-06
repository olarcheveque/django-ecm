# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from django.contrib import messages

from models import Catalog

class ContentMixin(SingleObjectMixin):
    model = Catalog

    def get_context_data(self, **kwargs):
        data = super(ContentMixin, self).get_context_data(**kwargs)
        edit_url = self.object.get_absolute_edit_url()
        view_url = self.object.get_absolute_url()

        actions = [
        ({'title': _("View"), 'url': view_url,
            'children': (),}),
        ({'title':  _("Edit"), 'url': edit_url,
            'children': (),}),
        ({'title':  _("State"), 'url': "#",
            'children': (
            ({'title': _('Draft'), 'url': "#"}),
            ({'title': _('Private'), 'url': "#"}),)})
            ]
        data['content_actions'] = actions
        return data

    def get_object(self, queryset=None):
        obj = super(ContentMixin, self).get_object(queryset)
        return obj.get_object()


class ContentDetailView(ContentMixin, DetailView):


    def get_template_names(self):
        return ("ecm/%s_detail.html" % self.object.content_type.model,
                "ecm/folder_detail.html",)

class ContentUpdateView(ContentMixin, UpdateView):
    model = Catalog

    def get_template_names(self):
        return ("ecm/%s_form.html" % self.object.content_type.model,
                "ecm/folder_form.html",)

    def form_valid(self, form):
        info = _("%s was successfully updated") % self.object.title
        messages.add_message(self.request, messages.INFO, info)
        return super(ContentUpdateView, self).form_valid(form)
        
    def form_invalid(self, form):
        info = _("There is error in the form")
        messages.add_message(self.request, messages.ERROR, info)
        return super(ContentUpdateView, self).form_invalid(form)
