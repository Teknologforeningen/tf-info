from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.conf import settings
import json
import urllib2, urllib
import datetime, random


cam_url =  settings.CAM_URL

def nextMeal():
  now = datetime.datetime.now()
  if now.weekday() < 5 and now.hour > 16:
    # after 16 show next day
    return 1
  else:
    # Else show current day
    return 0

def index(request, language='sv'):
  day = nextMeal()

  menu = cache.get('menu')


  if menu is None:
    try:
      response = urllib2.urlopen("http://api.teknolog.fi/taffa/%s/json/%d/"%(language, day))
      print "Fetched menu"
    except:
      return HttpResponse("Unable to access lunch API.", status=500)

    try:
      menu = json.load(response)
      cache.set('menu', menu, 500)
    except ValueError as e:
      return HttpResponse("Error parsing json from api", status=500)

  menu['cachebuster'] = random.randint(0, 99999)
  menu['cam_url'] = cam_url
  return render_to_response('dagsen/index.html', menu, context_instance=RequestContext(request))
