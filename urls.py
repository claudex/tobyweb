# -*- coding: utf-8 -*-
"""
Root url's map for the webapp project
"""
from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    
    (r'^', include('tobyweb.tribune.urls')),
)
        
# Display medias with the django wcgi only when Debug mode is actived
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^medias/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
