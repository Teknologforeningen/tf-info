from django.conf.urls import patterns, url
from kalender import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='calendar'),
)