from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.conf import settings

import urllib2

# Cache kept for
minutes = 30

@cache_page(60 * minutes)
def index(request):
	return render_to_response('arsfest/index.html', context_instance=RequestContext(request))
