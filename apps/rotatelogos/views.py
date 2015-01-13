from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.conf import settings

def index(request):

	return render_to_response('rotatelogos/index.html', {"img_url": img_url}, context_instance=RequestContext(request))
