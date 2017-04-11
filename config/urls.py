from django.conf.urls import patterns, include, url
from filebrowser.sites import site
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Redirect all to app
    url(r'^dagsen/', include('apps.dagsen.urls'), name='dagsen'),
    url(r'^reittiopas/', include('apps.reittiopas.urls'), name='reittiopas'),
    url(r'^weather/', include('apps.weather.urls'), name='weather'),
    url(r'^calendar/', include('apps.kalender.urls'), name='calendar'),
    url(r'^weathermap/', include('apps.weathermap.urls'), name='weathermap'),
    url(r'^rotatelogos/', include('apps.rotatelogos.urls'), name='rotatelogos'),
    url(r'^voteresults/', include('apps.voteresults.urls'), name='voteresults'),
    url(r'^arsfest/', include('apps.arsfest.urls'), name='arsfest'),
    url(r'^countdown/', include('apps.countdown.urls'), name='countdown'),

    # Wildcard
    url(r'^', include('manager.urls'), name='frontpage'),
)

# Enable Media and static for debugging
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)
