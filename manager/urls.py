from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from manager import views

urlpatterns = patterns('',

	#Root
    url(r'^$', views.index, name='frontpage'),

    url(r'^pages/(?P<index>\d+)/?$', views.get_page, name='get_page'),
    url(r'^pages/$', RedirectView.as_view(url='/pages/0/', permanent=False)),
    url(r'^(?P<url>https?://.+)', views.proxy, name='proxy_page')
)