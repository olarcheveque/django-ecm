# -*- coding: utf-8 -*-

from django.views.generic import ListView
from django.conf.urls.defaults import patterns, url

from django.contrib.auth.models import User, Group

from views.dispatcher import ECMView

urlpatterns = patterns('views',

    # Users Management
    url(r'users/$', ListView.as_view(
        model=User,
        template_name="ecm/users_list.html"),
        name="users_list"),
    url(r'groups/$', ListView.as_view(
        model=Group,
        template_name="ecm/groups_list.html"),
        name="groups_list"),

    # Entry point
    url(r'^$',
        ECMView.as_view(action='detail'),
        {'slugs': 'root'}),

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

)
