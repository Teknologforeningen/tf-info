from django.apps import AppConfig
from django.conf import settings
import os

class RotateLogosConfig(AppConfig):
    name = 'rotatelogos'
    verbose_name = "Rotate logos"
    def ready(self):
        #Check if folders exists, else create it
    	if not os.path.isdir(settings.MEDIA_ROOT + '/' + settings.FILEBROWSER_DIRECTORY + '/rotatelogos/' + '.thumbs/'):
    		os.makedirs(settings.MEDIA_ROOT + '/' + settings.FILEBROWSER_DIRECTORY + '/rotatelogos/' + '.thumbs/')
