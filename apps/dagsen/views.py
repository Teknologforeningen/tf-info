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
  return render_to_response('dagsen/index.html', menu, context_instance=RequestContext(request))

@cache_page(5)
def queuecam(request):
  try:
    stream=urllib.urlopen(cam_url)
    bytes=''
    for x in range(0, 1000):
      bytes+=stream.read(1024)
      a = bytes.find('\xff\xd8')
      b = bytes.find('\xff\xd9')
      if a!=-1 and b!=-1:
          jpg = bytes[a:b+2]
          bytes= bytes[b+2:]
          response = HttpResponse(jpg, content_type="image/jpeg")
          response['Cache-Control'] = 'max-age=0, no-cache, no-store'
          return response
  except:
    return HttpResponse("Unable to access camera.", status=500)

