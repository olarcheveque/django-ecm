# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from views import ContentDetailView, ContentUpdateView, ContentCreateView

urlpatterns = patterns('views',
    url(r'^$', ContentDetailView.as_view(), {'slugs': 'root'}),

    # Root level
    url(r'(?P<slugs>.*)/view$', ContentDetailView.as_view(),
        name="content_detail"),
    url(r'(?P<slugs>.*)/edit$', ContentUpdateView.as_view(),
    name="content_edit"),
    url(r'(?P<slugs>.*)/create/(?P<content_type>\w+)/$', ContentCreateView.as_view(),
    name="content_create"),
    url(r'(?P<slugs>.*)/$', ContentDetailView.as_view(),),
)
