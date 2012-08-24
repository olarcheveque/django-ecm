# -*- coding: utf-8 -*-

from django import template

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

register = template.Library()

@register.inclusion_tag('ecm/tags/navigation.html', takes_context=True)
def show_navigation(context, current_node):
    
    ancestors = list(current_node.get_ancestors())
    if len(ancestors) > 0:
        roots = list(ancestors[0].get_siblings())
    else:
        roots = []
    siblings = list(current_node.get_siblings(include_self=True))
    descendants = \
        list(current_node.get_children().filter(parent=current_node))
    if len(descendants) > 0:
        tree = []
        for s in siblings:
            if s.id == current_node.id:
                tree.append(s)
                tree += descendants
            else:
                tree.append(s)
    else:
        tree = siblings
    nodes = roots + ancestors + tree
    nodes = [n for n in nodes \
            if n.content_type.model_class().display_in_navigation]
    return {'nodes': nodes, 'current_node': current_node}

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
            )
    return {'nodes': nodes}
