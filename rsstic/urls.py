from django.conf.urls.defaults import *
from djangito.rsstic import views
from django.contrib.auth import views as authviews

urlpatterns = patterns('',

  # basic views
  url(r'^$', views.index, name='index'),
  url(r'^home', views.home, name='home'),
  url(r'^about', views.about, name='about'),
  url(r'^projects/$', views.projects, name='projects'),
  url(r'^login/$', 'django.contrib.auth.views.login'),
  url(r'^logout/$', 'django.contrib.auth.views.logout'),

  # project views
  url(r'^project/(?P<project_id>\d+)/$', views.project, name='project'),
  url(r'^project/(?P<project_id>\d+)/view/$', views.view, name='view project'),
  url(r'^project/(\d+)/feed/$', views.projectfeed, name='project feed'),

  # project verbs
  url(r'^project/(?P<project_id>\d+)/additem/$', views.additem, name='add item'),
  url(r'^project/(?P<project_id>\d+)/addfeed/$', views.addfeed, name='add feed'),
  url(r'^project/(\d+)/removefeed/(\d+)$', views.removefeed, name='remove feed'),
  url(r'^project/(\d+)/removitem/(\d+)$', views.removeitem, name='remove item'),

  # content views
  url(r'^feed/(?P<feed_id>\d+)/$', views.feed, name='feed'),

)
