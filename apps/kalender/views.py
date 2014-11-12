from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.conf import settings
from datetime import datetime
from datetime import date
from icalendar import Calendar, Event
import json
import urllib2
import pytz

# Cache kept for
minutes = 2

# URL of ical file from settings
ical_url = settings.KALENDER_ICAL

@cache_page(60 * minutes)
def index(request):
  try:
    response = urllib2.urlopen(ical_url)
    data = response.read()
  except:
    return HttpResponse("Unable to access calendar.", status=500)

  cal = Calendar.from_ical(data)
  now = timezone.now()
  today = date.today()

  events = []
  for event in cal.walk('vevent'):
    start = event.decoded('dtstart')
    e = { 'title': event.decoded('summary'),
          'start': start}

    # If start date is just a date (without time)
    if type(start) is type(today):
      if start > today:
        events.append(e)
    else:
      # Check if types (timezone or not) match
      try:
        start > now
      except TypeError:
        # Add timezone
        start = pytz.timezone("Europe/Helsinki").localize(start, is_dst=None)

      if start > now:
        events.append(e)

  return render_to_response('kalender/index.html', {"events":events[:8]}, context_instance=RequestContext(request))