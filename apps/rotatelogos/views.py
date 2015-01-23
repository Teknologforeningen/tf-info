from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.conf import settings
from models import Logo
import json, urllib


def index(request):

    return render_to_response('rotatelogos/index.html', context_instance=RequestContext(request))


def get_logo(request, index):
    i = int(index)

    all_entries = Logo.objects.all().order_by("id")

    if len(all_entries) == 0:
    	return HttpResponseNotFound()

    if i >= len(all_entries):
        i = 0

    response = json.dumps({"next": (i+1)%len(all_entries), "url": all_entries[i].thumbnail.url}, ensure_ascii=False, encoding='utf8')
    return HttpResponse(response, content_type='application/json; charset:utf-8')

    