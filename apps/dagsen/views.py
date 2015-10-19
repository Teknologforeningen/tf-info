from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
import json
import urllib2
import datetime

# Cache kept for
minutes = 10

def nextMeal():
  now = datetime.datetime.now()
  if now.weekday() < 5 and now.hour > 16:
    # after 16 show next day
    return 1
  else:
    # Else show current day
    return 0

@cache_page(60 * minutes)
def index(request, language='sv'):
  day = nextMeal()

  try:
    response = urllib2.urlopen("http://api.teknolog.fi/taffa/%s/json/%d/"%(language, day))
  except:
    return HttpResponse("Unable to access lunch API.", status=500)

  try:
    menu = json.load(response)
  except ValueError as e:
    return HttpResponse("Error parsing json from api", status=500)

  return render_to_response('dagsen/index.html',menu,context_instance=RequestContext(request))
