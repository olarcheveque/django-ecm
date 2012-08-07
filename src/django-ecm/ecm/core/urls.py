# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from views import ContentDetailView, ContentUpdateView, ContentCreateView

urlpatterns = patterns('views',
    url(r'^$', ContentDetailView.as_view(), {'slug': 'root'}),

    # Root level
    url(r'(?P<slug>\w+)/view$', ContentDetailView.as_view(),
        name="content_detail"),
    url(r'(?P<slug>\w+)/edit$', ContentUpdateView.as_view(),
    name="content_edit"),
    url(r'/(?P<parent_slug>\w+)/create/(?P<content_type>\w+)/$', ContentCreateView.as_view(),
    name="content_create"),
    url(r'(?P<slug>\w+)/$', ContentDetailView.as_view(),),

    # N level
    url(r'^(.*)/(?P<slug>\w+)/view$', ContentDetailView.as_view(),
        name="content_detail"),
    url(r'^(.*)/(?P<slug>\w+)/edit$', ContentUpdateView.as_view(),
    name="content_edit"),
    url(r'^(.*)/(?P<parent_slug>\w+)/create/(?P<content_type>\w+)/$', ContentCreateView.as_view(),
    name="content_create"),
    url(r'^(.*)[/]?(?P<slug>\w+)/$', ContentDetailView.as_view(),),

)
