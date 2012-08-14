# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from django.contrib.auth.models import User, Group

from models import ECMPermission

from ecm.core.views.roles import RoleListView
from ecm.core.views.roles import RoleCreateView
from ecm.core.views.dispatcher import ECMView

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
    url(r'permissions/$', ListView.as_view(
        model=ECMPermission,
        template_name="ecm/permissions/list.html"),
        name="permissions_list"),

    url(r'roles/$', RoleListView.as_view(),
        name="roles_list"),
    url(r'roles/create$', RoleCreateView.as_view(),
        name="roles_create"),

    # Entry point
    url(r'^$',
        ECMView.as_view(action='detail'),
        {'slugs': 'ecm'}),

    # Contents
    url(r'(?P<slugs>.*)/view$',
        ECMView.as_view(action='detail'),
        name="content_detail"),
    url(r'(?P<slugs>.*)/edit$',
        ECMView.as_view(action='update'),
        name="content_edit"),
    url(r'(?P<slugs>.*)/create/(?P<content_type>\w+)/$',
        ECMView.as_view(action='create'),
        name="content_create"),
    url(r'(?P<slugs>.*)/$',
        ECMView.as_view(action='detail'),
        name="content_detail"),

)

