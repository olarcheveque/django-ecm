# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class ViewSettings:
    """
    Settings for Content generic view.
    """
    exclude = ('parent', 'content_type', )
    allowed_content_type = ()

    def __init__(self, view):
        self.view = view

    def get_actions(self):
        """
        Return actions available for this content.
        """
        if self.view.object is None:
            return ()

        edit_url = self.view.object.get_absolute_edit_url()
        view_url = self.view.object.get_absolute_url()

        view = ({'title': _("View"), 'url': view_url, 'children': (), })
        edit = ({'title': _("Edit"), 'url': edit_url, 'children': (), })
        states = ({'title': _("State"), 'url': "#",
            'children': (
            ({'title': _('Draft'), 'url': "#"}),
            ({'title': _('Private'), 'url': "#"}),)})

        actions = [view, edit, states, ]

        allowed_content_type = self.get_allowed_content_type()
        if len(allowed_content_type) > 0:
            children = []
            context = "/".join(self.view.object.get_traversal_slugs())
            for ct in allowed_content_type:
                children.append({'title': _(ct),
                    'url': reverse('content_create',
                        args=[context,
                            ct]),
                    }
                    )
            add = ({'title': _("Add content"),
                    'url': '#',
                    'children': children})
            actions.append(add)

        return actions

    def get_exclude(self):
        """
        exclude fields from form
        """
        return self.exclude

    def get_allowed_content_type(self):
        return self.allowed_content_type


class FolderSettings(ViewSettings):
    """
    """
    allowed_content_type = ('Folder', 'Article', )


class ArticleSettings(ViewSettings):
    """
    """
    pass
