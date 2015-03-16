from django.conf.urls import patterns, url
from arsfest import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='arsfest'),
)
