from django.conf.urls import patterns, url
from countdown import views

urlpatterns = patterns('',
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<hour>[0-9]{2})/(?P<text>.+)/$', views.index, name='countdown'),
)