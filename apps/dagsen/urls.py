from django.conf.urls import patterns, url
from dagsen import views

urlpatterns = patterns('',

    #Root
    url(r'^$', views.index, name='lunch'),
    url(r'(?P<language>sv|en|fi)$', views.index, name='dagsen-lunch')
)