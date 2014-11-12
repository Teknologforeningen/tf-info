from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.conf import settings

import urllib2

"""
$i=0;
$count=file("counter.dat");
$i=$i+$count[0]+1;
if ($i > 1)
 $i=0;
file_put_contents("counter.dat", $i);

if ($i == 0)
{
$radar = curl_file_get_contents("http://testbed.fmi.fi");
$radar_d = explode("<img src=\"data", $radar);
$radar_t = explode("width=", $radar_d[1]);
}
else
{

echo "<div STYLE=\"position: absolute; top: 30px; left: 30px;\">";
 echo "<img src=\"http://testbed.fmi.fi/data".$radar_t[0].">";
}
"""

# Cache kept for
minutes = 3

@cache_page(60 * minutes)
def index(request):
	try:
		response = urllib2.urlopen("http://testbed.fmi.fi")
		data = response.read()
	except:
		return HttpResponse("Unable to access calendar.", status=500)

	print(data)
	img_url = data.split('src="data')[1]
	print(img_url)
	img_url = img_url.split('.png"')[0]
	print(img_url)
	img_url = "http://testbed.fmi.fi" + "/data" + img_url + ".png"
	print(img_url)


	return render_to_response('weathermap/index.html', {"img_url": img_url}, context_instance=RequestContext(request))
