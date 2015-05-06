from django.conf.urls.defaults import patterns, include, url
from djangito.rsstic import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangito.views.home', name='home'),
    # url(r'^djangito/', include('djangito.foo.urls')),
    url(r'^accounts/profile/', views.index, name='index'),
    url(r'^/', views.index, name='index'),
    url(r'^rsstic/', include('djangito.rsstic.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # ... other URL defs and includes here ....
    url(r'', include('django.contrib.auth.urls')),
)
