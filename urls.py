from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'toby.views.home', name='home'),
    # url(r'^toby/', include('toby.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$','tribune.views.index'),
    url(r'^(?P<tribune>.+)/preums/$', 'tribune.views.preums'),
    url(r'^(?P<tribune>.+)/preums/(?P<hour>.+)', 'tribune.views.preums'),
)
