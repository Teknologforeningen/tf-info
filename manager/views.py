from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
import json, urllib
from models import Page
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return render(request, 'infoskarm/index.html')

def get_page(request, index):
  i = int(index)
  count = Page.objects.count()

  if i >= count:
    return HttpResponseNotFound()

  page = Page.objects.get(order=i)

  # Find next active page
  for x in range(count):
    next_page = (i+x+1)%count
    if page is not None and page.is_active():
      if page.image:
        # Return a response that redirects to baseurl/image/page_id
        url = request.build_absolute_uri("/image/" + str(page.pk))
        response = json.dumps({"next": next_page, "url": url, "duration": page.duration}, ensure_ascii=False, encoding='utf8')
      else:
        response = json.dumps({"next": next_page, "url": page.url, "duration": page.duration}, ensure_ascii=False, encoding='utf8')
      return HttpResponse(response, content_type='application/json; charset:utf-8')
    else:
      page = Page.objects.get(order=next_page)

  # Not a single active page found.
  return HttpResponseNotFound()

def get_image(request, page):
    page = Page.objects.get(pk=page)
    return render_to_response('infoskarm/image.html',
        {
            "image_url": page.image.url,
            "hide_top": page.hide_top_bar,
            "hide_bottom": page.hide_bottom_bar
        },
         context_instance=RequestContext(request))

def proxy(request, url):
  return render_to_response('infoskarm/iframe.html', {"url": url}, context_instance=RequestContext(request))
