from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.views.decorators.cache import cache_page

import urllib2

"""

Takes in results from a vote in the following format:

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body>
0:1<br>1:0<br>2:0<br>3:0<br>4:0<br>5:0<br>9:0<br></body>
</html>

Parses and adds colors

"""


class Result:
	def __init__(self, voteid, count):
		self.id = int (voteid)
		self.count = int(count)
		self.color = "#0F0F0F"
		self.size = 0
		self.pos = 0
	
	def add_votes(self, add_count):
		self.count += add_count

	def set_color(self, color):
		self.color = color

@cache_page(60 * 10)
def index(request):
	try:
		response = urllib2.urlopen(settings.VOTERESULTS_URL)
		data = response.read()
	except:
		return HttpResponse("Unable to access stats.", status=500)

	result = data.split("<body>")[1].split("</body>")[0].split("<br>")

	votes = []

	for x in result:
		x = x.replace("\n","")
		if len(x) == 0:
			continue

		xId = x.split(":")[0]
		xCount = x.split(":")[1]

		if xId == "1" or xId == "2":
			votes[0].add_votes(int(xCount))
		else:
			votes.append(Result(xId, xCount))

	for x in votes:
		if x.id == 0:
			x.set_color("#FF9900")
		elif x.id == 3:
			x.id = 1
			x.set_color("#6699FF")
		elif x.id == 4:
			x.id = 2
			x.set_color("#66FF33")
		elif x.id == 5:
			x.id = 4
			x.set_color("#835C3B")
		elif x.id == 9:
			x.id = 3
			x.set_color("#FF1919")

		x.pos = x.id *22

		if int(x.count) > 20:
			x.size = 95

		else:
			x.size = int((float(x.count) / 20) * 95)

	width = votes[-1].pos + 22 + 10

	return render_to_response('voteresults/index.html', {"votes": votes, "width": width}, context_instance=RequestContext(request))
