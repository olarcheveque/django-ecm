# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView

from django.contrib import messages

from ecm.core.views.mixin import TraversableView, ContentMixin, \
        ContentFormMixin


class ContentDetailView(TraversableView, ContentMixin, DetailView):

    def get_context_data(self, **kwargs):
        data = super(ContentDetailView, self).get_context_data(**kwargs)
        children = self.object.get_children()\
                .select_related('content_type').all()
        node = self.kwargs.get('node')
        properties = []
        for f in node._meta.fields:
            properties.append((f.name, getattr(node, f.name), ))
        extra = {'children': children,
            'properties': properties,
            }
        data.update(extra)
        return data


class ContentUpdateView(TraversableView,
        ContentMixin, ContentFormMixin, UpdateView):
    pass


class ContentDeleteView(TraversableView, ContentMixin,
        DeleteView):

    def get_success_url(self):
        return self.kwargs.get('node').parent.get_absolute_url()

    def form_valid(self, form):
        info = _("%s was successfully created") % self.title
        messages.add_message(self.request, messages.INFO, info)
        return super(ContentDeleteView, self).form_valid(form)


class ContentCreateView(TraversableView,
        ContentMixin, ContentFormMixin, CreateView):

    def form_valid(self, form):
        """
        Create content using the context.
        """
        content_type = ContentType.objects.get(
                model=self.kwargs.get('content_type').lower()
                )
        obj = form.save(commit=False)
        obj.content_type = content_type
        obj.parent = self.kwargs.get('traversal')[-1]
        obj.save()
        self.object = obj
        
        info = _("%s was successfully created") % obj.title
        messages.add_message(self.request, messages.INFO, info)
        return HttpResponseRedirect(self.get_success_url())
