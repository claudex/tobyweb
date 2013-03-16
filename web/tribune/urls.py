# -*- coding: utf-8 -*-
"""
Root url's map for the "tribune" application
"""
from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('tribune.views',
    url(r'^$', TemplateView.as_view(template_name='tribune/index.html'), name='tobyweb-index'),
    #Preums
    url(r'^(?P<tribune>.+)/preums/$', 'preums', name='tobyweb-preums-index'),
    url(r'^(?P<tribune>.+)/preums/(?P<hour>.+)', 'preums', name='tobyweb-preums-details'),
    #Chasse
    url(r'^(?P<tribune>.+)/chasse/$', 'chasse', name= 'tobyweb-chasse-index'),
    #Cps
    url(r'^(?P<tribune>.+)/cps$', 'cps', name='tobyweb-cps-index'),
    url(r'^(?P<tribune>.+)/cps.json/$','cps_json'),
    
    #Daemon posts
    url(r'^post', 'web.views.post'),
)
