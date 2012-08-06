# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.inclusion_tag('ecm/tags/navigation.html', takes_context=True)
def show_navigation(context, node, level=1):
    nodes = node.get_descendants()
    return {'nodes': nodes}
