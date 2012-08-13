# -*- coding: utf-8 -*-

from django import template

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

register = template.Library()

@register.inclusion_tag('ecm/tags/navigation.html', takes_context=True)
def show_navigation(context, current_node, types=None):
    
    nodes = list(current_node.get_ancestors()) + [current_node, ]
    descendants = current_node.get_children().select_related('content_type')

    if types is None:
        nodes += [n for n in descendants]
        return {'nodes': nodes}
    else:
        nodes += [n for n in descendants if n.content_type.model in
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
             },
            {'title': _("Permissions"),
             'url': reverse('permissions_list'),
             'children': (),
             },
            {'title': _("Roles"),
             'url': reverse('roles_list'),
             'children': (),
             },
            )
    return {'nodes': nodes}
