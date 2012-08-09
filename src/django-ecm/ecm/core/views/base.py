# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, UpdateView, CreateView

from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

from ecm.core.views.mixin import TraversableView, ContentMixin, ContentFormMixin

class ContentDetailView(TraversableView, ContentMixin, DetailView):

    def get_template_names(self):
        return ("ecm/%s_detail.html" % self.object.content_type.model,
                "ecm/folder_detail.html",)

class ContentUpdateView(TraversableView, ContentMixin, ContentFormMixin, UpdateView):

    def get_template_names(self):
        return ("ecm/%s_edit.html" % self.object.content_type.model,
                "ecm/folder_edit.html",)


class ContentCreateView(ContentMixin, ContentFormMixin, CreateView):

    def get_template_names(self):
        return ("ecm/%s_create.html" % self.model.__class__.__name__,
                "ecm/folder_create.html",)

    def _initialize(self):
        type = self.kwargs.get('content_type').lower()
        self.content_type = ContentType.objects.get(model=type)
        self.model = self.content_type.model_class()
        self.parent = self.get_traversal()[-1]
        self._setup_settings(type, **{'content': self.parent})

    def get(self, request, *args, **kwargs):
        self._initialize()
        return super(ContentCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self._initialize()
        return super(ContentCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Create content using the context.
        """
        obj = form.save(commit=False)
        obj.content_type = self.content_type
        obj.parent = self.parent
        obj.save()
        self.object = obj

        info = _("%s was successfully created") % obj.title
        messages.add_message(self.request, messages.INFO, info)
        return HttpResponseRedirect(self.get_success_url())
