# -- coding: UTF-8 ---
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.cache import cache_page
import json, re 
import urllib2

WEATHER_LOCATION=settings.WEATHER_LOCATION
WEATHER_APIKEY=settings.WEATHER_APIKEY

@cache_page(60 * 5) # 5 minutes
def index(request):


	# Forecast
	url = 'http://api.openweathermap.org/data/2.5/weather?q=%s&APPID=%s'% (WEATHER_LOCATION, WEATHER_APIKEY)
	try:
		response = urllib2.urlopen(url)
	except Exception as e:
		return HttpResponse("Unable to access openweathermap API.", status=500)

	try:
		weather = json.load(response)
	except ValueError as e:
		return HttpResponse("Error parsing json from weather response.", status=500)

	weather_id = weather['weather'][0]['id']
	classes = "climacon %s"%OPENWEATHERMAP_TO_CLIMACON[int(weather_id)]

	# Outside
	try:
		response = urllib2.urlopen('http://outside.aalto.fi/temp.html')
	except Exception as e:
		return HttpResponse("Unable to access outside.aalo.fi .", status=500)

	temp = int(round(float(re.search(r': (?P<temp>-?\d+\.\d+) °C', response.read()).group('temp'))))


	return render_to_response('weather/small.html', {"temp": temp, "classes": classes}, context_instance=RequestContext(request))


OPENWEATHERMAP_TO_CLIMACON={
	200: "lightning",
	201: "lightning",
	202: "lightning",
	210: "lightning",
	211: "lightning",
	212: "lightning",
	221: "lightning",
	230: "lightning sun",
	231: "lightning sun",
	232: "lightning",
	300: "drizzle sun",
	301: "drizzle",
	302: "showers",
	310: "showers sun",
	311: "showers sun",
	312: "showers",
	313: "showers",
	314: "rain",
	321: "showers",
	500: "rain sun",
	501: "rain",
	502: "rain",
	503: "downpour",
	504: "downpour",
	511: "hail",
	520: "rain",
	520: "showers",
	521: "showers",
	522: "rain",
	531: "rain",
	600: "snow sun",
	601: "snow",
	602: "snow",
	611: "snow",
	612: "snow",
	615: "flurries",
	616: "flurries",
	620: "snow",
	621: "snow",
	622: "snow",
	701: "fog",
	711: "fog",
	721: "haze",
	731: "tornado",
	741: "fog",
	751: "tornado",
	761: "tornado",
	762: "tornado",
	771: "tornado",
	781: "tornado",
	800: "sun",
	801: "sun",
	802: "cloud sun",
	803: "cloud sun",
	804: "cloud sun",
	900: "tornado",
	901: "tornado",
	902: "tornado",
	903: "snowflake",
	904: "thermometer full",
	905: "wind",
	906: "hail",
	950: "sun",
	951: "sun",
	952: "wind cloud sun",
	953: "wind cloud sun",
	954: "wind",
	955: "wind",
	956: "wind",
	957: "wind",
	958: "tornado",
	959: "tornado",
	960: "tornado",
	961: "tornado",
	962: "tornado",
}