from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','tribune.views.index'),
    url(r'^(?P<tribune>.+)/preums/$', 'tribune.views.preums'),
    url(r'^(?P<tribune>.+)/preums/(?P<hour>.+)', 'tribune.views.preums'),
)
