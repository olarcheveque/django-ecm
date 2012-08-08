# -*- coding: utf-8 -*-

from django.forms import models as model_forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, UpdateView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ModelFormMixin

from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

from models import Catalog

class ContentMixin(SingleObjectMixin):
    model = Catalog
    settings = None

    def get_traversal(self):
        slugs = self.kwargs.get('slugs').split('/')
        return Catalog.objects.filter(slug__in=slugs)

    def _setup_settings(self, model):
        settings_klass = "%sSettings" % model.title()
        for f in settings.ECM_VIEWS_SETTINGS:
            mod = __import__(f, fromlist='.')
            try:
                self.settings = getattr(mod, settings_klass)(view=self)
                break
            except:
                pass
        if self.settings is None:
            raise Exception('There is no settings found for ECM view %s' %
                    settings_klass)

    def get_context_data(self, **kwargs):
        data = super(ContentMixin, self).get_context_data(**kwargs)
        data['content_actions'] = self.settings.get_actions()
        data['content_type'] = self.model._meta.verbose_name
        return data

    def get_object(self, queryset=None):
        """
        Fix the model dynamically
        """
        obj = self.get_traversal()[0]

        # Setup content Type
        self.content_type = obj.content_type
        self.model = self.content_type.model_class()
        self._setup_settings(obj.content_type.model)

        return obj.get_object()


class ContentDetailView(ContentMixin, DetailView):

    def get_template_names(self):
        return ("ecm/%s_detail.html" % self.object.content_type.model,
                "ecm/folder_detail.html",)

class ContentFormView(ModelFormMixin):

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        if self.form_class:
            return self.form_class
        else:
            if self.model is not None:
                # If a model has been explicitly provided, use it
                model = self.model
            elif hasattr(self, 'object') and self.object is not None:
                # If this view is operating on a single object, use
                # the class of that object
                model = self.object.__class__
            else:
                # Try to get a queryset and extract the model class
                # from that
                model = self.get_queryset().model
            return model_forms.modelform_factory(model,
                    **{'exclude': self.settings.get_exclude()})

    def form_valid(self, form):
        info = _("%s was successfully updated") % self.object.title
        messages.add_message(self.request, messages.INFO, info)
        return super(ContentFormView, self).form_valid(form)

    def form_invalid(self, form):
        info = _("There is error in the form")
        messages.add_message(self.request, messages.ERROR, info)
        return super(ContentFormView, self).form_invalid(form)


class ContentUpdateView(ContentMixin, ContentFormView, UpdateView):

    def get_template_names(self):
        return ("ecm/%s_edit.html" % self.object.content_type.model,
                "ecm/folder_edit.html",)


class ContentCreateView(ContentMixin, ContentFormView, CreateView):

    def get_template_names(self):
        return ("ecm/%s_create.html" % self.model.__class__.__name__,
                "ecm/folder_create.html",)

    def _initialize(self):
        type = self.kwargs.get('content_type').lower()
        self.content_type = ContentType.objects.get(model=type)
        self.model = self.content_type.model_class()
        self._setup_settings(type)

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
        parent_slug = self.kwargs.get('slugs').split('/')[-1]
        obj = form.save(commit=False)
        obj.content_type = self.content_type
        obj.parent = Catalog.objects.get(slug=parent_slug)
        obj.save()
        self.object = obj

        info = _("%s was successfully created") % obj.title
        messages.add_message(self.request, messages.INFO, info)
        return HttpResponseRedirect(self.get_success_url())
