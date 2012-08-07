# -*- coding: utf-8 -*-
from ecm.core.models import Catalog
from django import template

register = template.Library()

@register.inclusion_tag('ecm/tags/navigation.html', takes_context=True)
def show_navigation(context, level=1, types=None):
    root = Catalog.objects.get(parent__isnull=True)
    if types is None:
        nodes = [n for n in root.get_descendants()]
        return {'nodes': nodes}
    else:
        nodes = [n for n in root.get_descendants() if n.content_type.model in
                types]
        return {'nodes': nodes}
