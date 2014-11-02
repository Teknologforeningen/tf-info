from django.conf.urls import patterns, url
from weather import views

urlpatterns = patterns('',
    url(r'^small/$', views.index, name='weather-small'),
)