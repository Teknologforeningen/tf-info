from django.conf.urls import patterns, url
from rotatelogos import views
from django.contrib import admin

# Enable custom admin page
admin.site.index_template = 'admin/rotatelogos_index.html'

urlpatterns = patterns('',
  url(r'^$', views.index, name='rotatelogos'),
  url(r'refresha', views.refresha, name ='rotaterefresha'),
)
