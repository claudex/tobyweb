# -*- coding: utf-8 -*-
"""
Root url's map for the "tribune" application
"""
from django.conf.urls.defaults import *

urlpatterns = patterns('tribune.views',
    url(r'^$','index', name='tobyweb-index'),
    url(r'^(?P<tribune>.+)/preums/$', 'preums', name='tobyweb-preums-index'),
    url(r'^(?P<tribune>.+)/preums/(?P<hour>.+)', 'preums', name='tobyweb-preums-details'),
)
