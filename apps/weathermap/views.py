from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.conf import settings

import urllib2

# Cache kept for
minutes = 2

@cache_page(60 * minutes)
def index(request):
	try:
		response = urllib2.urlopen("http://testbed.fmi.fi")
		data = response.read()
	except:
		return HttpResponse("Unable to access fmi for weathermap", status=500)

	img_url = data.split('src="data')[1].split('.png"')[0]
	img_url = "http://testbed.fmi.fi" + "/data" + img_url + ".png"

	return render_to_response('weathermap/index.html', {"img_url": img_url}, context_instance=RequestContext(request))
