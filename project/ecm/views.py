# -*- coding: utf-8 -*-

from django.views.generic import DetailView, UpdateView

from models import Catalog


class ContentDetailView(DetailView):
    model = Catalog

    def get_context_data(self, **kwargs):
        data = super(ContentDetailView, self).get_context_data(**kwargs)
        return data

    def get_object(self, queryset=None):
        obj = super(ContentDetailView, self).get_object(queryset)
        return obj.get_object()

    def get_template_names(self):
        return ("ecm/%s_detail.html" % self.object.content_type.model,
                "ecm/folder_detail.html",)

class ContentUpdateView(UpdateView):
    model = Catalog
    template_name = "ecm/folder_form.html"
