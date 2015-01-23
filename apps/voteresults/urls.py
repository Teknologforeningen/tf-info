from django.conf.urls import patterns, url
from voteresults import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='voteresults'),
)
