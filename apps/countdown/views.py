from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.utils.http import urlencode

import json
import urllib2



def index(request, year, month, day, hour, text):

	params = {
		'year': year,
		'month': int(month) - 1, #JS takes months in retarded format...
		'day': day,
		'text': text,
		'hour': int(hour)
	}

	return render_to_response('countdown/index.html', params, context_instance=RequestContext(request))