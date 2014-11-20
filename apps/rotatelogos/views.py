from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.conf import settings

import glob
import os
from PIL import Image

def index(request):

	return render_to_response('rotatelogos/index.html', {"img_url": img_url}, context_instance=RequestContext(request))

def refresha(request):
	status = ""
	# Reads in logos from the folder, then create or remove thumbnails
	# TODO: User rights instead of just authentication...
	if not request.user.is_authenticated():
		status = "Refresh failed, not authenticated \n"
		return render_to_response('rotatelogos/status.html', {"status":status}, context_instance=RequestContext(request))
	
	image_formats = ["gif","png","tif","jpeg","jpg"]

	image_path = settings.MEDIA_ROOT + '/' + settings.FILEBROWSER_DIRECTORY + '/rotatelogos/*'
	thumbs_path = settings.MEDIA_ROOT + '/' + settings.FILEBROWSER_DIRECTORY + '/rotatelogos/.thumbs/*'

	image_path = image_path.replace("//","/")
	thumbs_path = thumbs_path.replace("//","/")
	
	image_list = glob.glob(image_path)
	thumbs_list = glob.glob(thumbs_path)
	image_list_names = {}
	thumbs_list_names = {}

	print image_list 
	print thumbs_list
	

	for x in thumbs_list:
		thumbs_list_names[x] = x.split("/")[-1]

	for x in image_list:
		image_list_names[x] = x.split("/")[-1]

	print image_list_names 
	print thumbs_list_names 

	for x,y in image_list_names.iteritems():
		if y not in thumbs_list_names.values() and y.split(".")[-1].lower() in image_formats:
			#Make thumbnail
			outfile = settings.MEDIA_ROOT + \
							'/' + settings.FILEBROWSER_DIRECTORY + \
							'/rotatelogos/.thumbs/' + y
			infile = x

			im = Image.open(infile)
			im.thumbnail((300,90), Image.ANTIALIAS)
			im.save(outfile, "JPEG")
			status += "Added " + y + " thumbnail \n"


	for x,y in thumbs_list_names.iteritems():
		if y not in image_list_names.values() and y.split(".")[-1].lower() in image_formats:
			#Remove thumbnail
			os.remove(x)
			status += "Removed thumbnail " + y +"\n"

	status += "All done.. :)"
	return render_to_response('rotatelogos/status.html', {"status":status}, context_instance=RequestContext(request))