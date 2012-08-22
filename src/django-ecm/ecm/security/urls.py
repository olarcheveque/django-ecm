# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from django.contrib.auth.models import User, Group

from views import PermissionListView

urlpatterns = patterns(
    '',

    # Users Management
    url(r'users/$', ListView.as_view(
        model=User,
        template_name="ecm/users/list.html"),
        name="users_list"),
    url(r'groups/$', ListView.as_view(
        model=Group,
        template_name="ecm/groups/list.html"),
        name="groups_list"),

    # Security Management
    url(r'permissions/$', PermissionListView.as_view(),
        name="permissions_list"),
)
