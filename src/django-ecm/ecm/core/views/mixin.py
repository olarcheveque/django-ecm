# -*- coding: utf-8 -*-

from django.forms import models as model_forms
from django.conf import settings
from django.views.generic.base import View
from django.views.generic.edit import ModelFormMixin
from django.views.generic.detail import SingleObjectMixin

from django.contrib import messages

from ecm.core.models import Catalog

class TraversableView(View):
    """
    """
    def get_context_data(self, **kwargs):
        data = super(TraversableView, self).get_context_data(**kwargs)
        data.update(self.kwargs)
        return data

    def get_slugs(self):
        """
        Get parent slugs list from URL.
        """
        return [t.slug for t in self.kwargs.get('traversal')]

    def get_traversal(self):
        """
        Load catalog brains from URL slugs.
        """
        return self.kwargs.get('traversal')


class ContentMixin(SingleObjectMixin):
    model = Catalog
    settings = None

    def _setup_settings(self, model, **kwargs):
        settings_klass = "%sSettings" % model.title()
        for f in settings.ECM_VIEWS_SETTINGS:
            mod = __import__(f, fromlist='.')
            try:
                self.settings = getattr(mod,
                        settings_klass)(**kwargs)
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
        obj = self.get_traversal()[-1]

        # Setup content Type
        self.content_type = obj.content_type
        self.model = self.content_type.model_class()
        self._setup_settings(obj.content_type.model, **{'content': obj})

        return obj.get_object()


class ContentFormMixin(ModelFormMixin):

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
        return super(ContentFormMixin, self).form_valid(form)

    def form_invalid(self, form):
        info = _("There is error in the form")
        messages.add_message(self.request, messages.ERROR, info)
        return super(ContentFormMixin, self).form_invalid(form)


