# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from django.contrib.auth.models import User, Group

from views import RoleListView, RoleCreateView, \
    WorkflowListView, WorkflowCreateView, \
    PermissionListView

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
    url(r'roles/$', RoleListView.as_view(),
        name="roles_list"),
    url(r'roles/create$', RoleCreateView.as_view(),
        name="roles_create"),

    # Workflow Management
    url(r'workflows/$', WorkflowListView.as_view(),
        name="workflows_list"),
    url(r'workflows/create$', WorkflowCreateView.as_view(),
        name="workflows_create"),
)
