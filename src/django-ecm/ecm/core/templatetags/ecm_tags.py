# -*- coding: utf-8 -*-

from django import template

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from ecm.core.models import Catalog

register = template.Library()

@register.inclusion_tag('ecm/tags/navigation.html', takes_context=True)
def show_navigation(context, types=None):
    root = Catalog.objects.get(parent__isnull=True)
    nodes = [root, ]
    if types is None:
        nodes += [n for n in root.get_descendants()]
        return {'nodes': nodes}
    else:
        nodes += [n for n in root.get_descendants() if n.content_type.model in
                types]
        return {'nodes': nodes}

@register.inclusion_tag('ecm/tags/navbar.html', takes_context=True)
def show_navbar(context, ):
    nodes = (
            {'title': _("Users"),
             'url': reverse('users_list'),
             'children': (),
             },
            {'title': _("Groups"),
             'url': reverse('groups_list'),
             'children': (),
             },)
    return {'nodes': nodes}
