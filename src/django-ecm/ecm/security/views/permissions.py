# -*- coding: utf-8 -*-

from django.views.generic import ListView


from ecm.security.models import ECMPermission


class PermissionListView(ListView):
    model = ECMPermission
    template_name = "ecm/permissions/list.html"
