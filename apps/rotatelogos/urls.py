from django.conf.urls import patterns, url
from apps.rotatelogos import views
from django.views.generic.base import RedirectView


urlpatterns = patterns('',
	#url(r'^$', views.index, name='rotatelogos'),
	url(r'^(?P<index>\d+)/?$', views.get_logo, name='get_logo'),
	url(r'^$', RedirectView.as_view(url='/rotatelogos/0/', permanent=False)),
)
