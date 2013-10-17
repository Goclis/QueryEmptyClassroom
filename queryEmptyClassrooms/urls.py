# encoding: UTF-8

from django.conf.urls import patterns, include, url
import queryEmptyClassrooms.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^queryEmptyClassrooms/query/$', queryEmptyClassrooms.views.queryEmptyClassrooms),
	(r'^queryEmptyClassrooms/index/$', queryEmptyClassrooms.views.index),
    (r'^queryEmptyClassrooms/about/$', queryEmptyClassrooms.views.about),
    (r'^app/classroom/$', queryEmptyClassrooms.views.shortIndex) # 方便记忆的链接
    # Examples:
    # url(r'^$', 'queryEmptyClassrooms.views.home', name='home'),
    # url(r'^queryEmptyClassrooms/', include('queryEmptyClassrooms.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
