from django.conf.urls import patterns, url
from rotatelogos import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='rotatelogos'),
)
