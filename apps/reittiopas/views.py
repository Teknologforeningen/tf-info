from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from operator import itemgetter
from datetime import datetime, timedelta
import json
import urllib2
import re

# Get API user and token from settings
user = settings.REITTIOPAS_USER
token = settings.REITTIOPAS_TOKEN
stops = settings.REITTIOPAS_STOPS

def index(request):
	all_departures = []

	for stop in stops:
		try:
			response = urllib2.urlopen("http://api.reittiopas.fi/hsl/prod/?user=%s&pass=%s&request=stop&code=%s"%(user,token,stop))
		except:
			return HttpResponse("Unable to access reittiopas API.", status=500)

		try:
			stop_departures = json.load(response)[0]
		except ValueError as e:
			return HttpResponse("Error parsing json from reittiopas", status=500)

		# Parse line destinations from codes
		lines_dict = {}
		for item in stop_departures['lines']:
			parts = item.split(':')
			lines_dict[parts[0]] = parts[1]

		# Parse departures
		departures = []
		for departure in stop_departures['departures']:
			# Convert code to actual line number
			departure['line'] = re.sub(r'^\d0*(\d?\w*) .*', r'\1',departure['code'])

			departure['stop'] = stop_departures['name_fi']

			# Add destination name to departure item
			departure['dest'] = lines_dict[departure['code']]

			# Create datetime object to sort departures by
			if departure['time'] >= 2400:
				departure['time'] = departure['time']-2400
				dt = datetime.strptime('%d%d'%(departure['date'], departure['time']), "%Y%m%d%H%M")
				departure['datetime'] = dt + timedelta(days=1)
			else:
				departure['datetime'] = datetime.strptime('%d%d'%(departure['date'], departure['time']), "%Y%m%d%H%M")

			departures.append(departure)

		all_departures = all_departures + departures

	sorted_departures = sorted(all_departures, key=itemgetter('datetime'))[:10]

	return render_to_response('reittiopas/index.html', {"departures": sorted_departures}, context_instance=RequestContext(request))