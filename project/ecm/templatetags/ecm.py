# -*- coding: utf-8 -*-

from project.ecm.models import Catalog
from django import template

register = template.Library()

@register.inclusion_tag('ecm/tags/navigation.html', takes_context=True)
def show_navigation(context, level=1):
    root = Catalog.objects.get(parent__isnull=True)
    nodes = root.get_descendants()
    return {'nodes': nodes}
