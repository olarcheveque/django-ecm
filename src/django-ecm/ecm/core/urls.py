# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

from ecm.core.views.dispatcher import ECMView

urlpatterns = patterns(
    '',

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
    url(r'(?P<slugs>.*)/delete$',
        ECMView.as_view(action='delete'),
        name="content_delete"),
    url(r'(?P<slugs>.*)/create/(?P<content_type>\w+)/$',
        ECMView.as_view(action='create'),
        name="content_create"),
    url(r'(?P<slugs>.*)/$',
        ECMView.as_view(action='detail'),
        name="content_detail"),

)

