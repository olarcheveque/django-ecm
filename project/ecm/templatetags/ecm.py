# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.inclusion_tag('ecm/tags/navigation.html', takes_context=True)
def show_navigation(context, node, level=1):
    root = node.get_root()
    nodes = root.get_descendants()
    return {'nodes': nodes}
