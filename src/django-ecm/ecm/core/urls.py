# -*- coding: utf-8 -*-

from django.views.generic import ListView
from django.conf.urls.defaults import patterns, url

from django.contrib.auth.models import User, Group

from views import ContentDetailView, ContentUpdateView, ContentCreateView

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
    url(r'^$', ContentDetailView.as_view(), {'slugs': 'root'}),

    # Contents
    url(r'(?P<slugs>.*)/view$', ContentDetailView.as_view(),
        name="content_detail"),
    url(r'(?P<slugs>.*)/edit$', ContentUpdateView.as_view(),
    name="content_edit"),
    url(r'(?P<slugs>.*)/create/(?P<content_type>\w+)/$', ContentCreateView.as_view(),
    name="content_create"),
    url(r'(?P<slugs>.*)/$', ContentDetailView.as_view(),),

)
