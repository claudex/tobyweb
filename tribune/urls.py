# -*- coding: utf-8 -*-
"""
Root url's map for the "tribune" application
"""
from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('tribune.views',
    url(r'^$', TemplateView.as_view(template_name='tribune/index.html'), name='tobyweb-index'),
    url(r'^(?P<tribune>.+)/preums/$', 'preums', name='tobyweb-preums-index'),
    url(r'^(?P<tribune>.+)/preums/(?P<hour>.+)', 'preums', name='tobyweb-preums-details'),
    url(r'^(?P<tribune>.+)/chasse/$', 'chasse', name= 'tobyweb-chasse-index'),
)
