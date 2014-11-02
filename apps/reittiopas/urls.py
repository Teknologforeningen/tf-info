from django.conf.urls import patterns, url
from reittiopas import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='reittiopas'),
)