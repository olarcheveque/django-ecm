# -*- coding: utf-8 -*-

from django.forms import models as model_forms
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.views.generic.edit import ModelFormMixin
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from django.contrib import messages


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
    actions = None
    exclude = ('parent', 'content_type', 'slug', )

    def get_template_names(self):
        action = self.kwargs.get('action')
        model = self.kwargs.get('model')
        tpls = ("ecm/%s/%s.html" % (model.__name__.lower(), action),
                "ecm/folder/%s.html" % action,)
        return tpls

    def get_exclude(self):
        """
        exclude fields from form
        """
        return self.exclude

    def get_allowed_content_types(self):
        if hasattr(self.object, 'allowed_content_types'):
            return self.object.allowed_content_types
        else:
            return ()

    def get_actions(self):
        if self.actions is not None:
            return self.actions

        if self.object is None:
            return ()
        
        actions = []

        current_url = self.request.get_full_path()
        edit_url = self.object.get_absolute_edit_url()
        view_url = self.object.get_absolute_url()
        delete_url = self.object.get_absolute_delete_url()

        def add_action(url, action_title):
            if current_url != url:
                view = ({
                    'title': action_title,
                    'url': url,
                    'children': (),
                    })
                actions.append(view)

        add_action(view_url, _("View"))
        add_action(edit_url, _("Edit"))
        add_action(delete_url, _("Delete"))

        allowed_content_type = self.get_allowed_content_types()
        if len(allowed_content_type) > 0:
            children = []
            context = "/".join(self.object.get_traversal_slugs())
            for ct_name in allowed_content_type:
                ct = ContentType.objects.get(model=ct_name)
                title = ct.model_class()._meta.verbose_name
                children.append({'title': title,
                    'url': reverse('content_create',
                        args=[context, ct_name]),
                    }
                    )
            add = ({'title': _("Add content"),
                    'url': '#',
                    'children': children})
            actions.append(add)
        return actions

    def get_context_data(self, **kwargs):
        data = super(ContentMixin, self).get_context_data(**kwargs)
        data['actions'] = self.get_actions()
        data['content_type'] = self.kwargs.get('node').content_type.model
        return data

    def get_object(self, queryset=None):
        """
        Fix the model dynamically
        """
        obj = self.kwargs.get('node')
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
            return model_forms.modelform_factory(model, **{'exclude':
                self.get_exclude()})

    def form_valid(self, form):
        info = _("%s was successfully updated") % self.object.title
        messages.add_message(self.request, messages.INFO, info)
        return super(ContentFormMixin, self).form_valid(form)

    def form_invalid(self, form):
        info = _("There is error in the form")
        messages.add_message(self.request, messages.ERROR, info)
        return super(ContentFormMixin, self).form_invalid(form)


