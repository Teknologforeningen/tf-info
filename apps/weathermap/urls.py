from django.conf.urls import patterns, url
from weathermap import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='weathermap'),
)
