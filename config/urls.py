from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Redirect all to app
    url(r'^dagsen/', include('apps.dagsen.urls'), name='dagsen'),
    url(r'^reittiopas/', include('apps.reittiopas.urls'), name='reittiopas'),
    url(r'^weather/', include('apps.weather.urls'), name='weather'),
    url(r'^calendar/', include('apps.kalender.urls'), name='calendar'),

    # Wildcard
    url(r'^', include('manager.urls'), name='frontpage'),
)
