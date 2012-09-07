# -*- coding: utf-8 -*-

from django import template

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

register = template.Library()

@register.inclusion_tag('ecm/tags/navigation.html', takes_context=True)
def show_navigation(context, current_node):
    
    def sort_nodes(x, y):
        return cmp(x.title, y.title)

    ancestors = list(current_node.get_ancestors())
    nodes = []

    if len(ancestors) == 0:
        ancestors = [current_node, ]
    ancestors = sorted(ancestors, cmp=sort_nodes)

    for ancestor in ancestors:
        siblings = ancestor.get_siblings(include_self=True)
        siblings = sorted(siblings, cmp=sort_nodes)
        for s in siblings:
            nodes.append(s)
            if s == ancestor:
                nodes += list(ancestor.get_children())

    nodes = [n for n in nodes \
            if n.content_type.model_class().display_in_navigation]

    return {
        'nodes': nodes,
        'current_node': current_node,
        }

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
