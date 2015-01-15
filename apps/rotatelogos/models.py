from django.db import models
from django.conf import settings

#Create thumbnail:
from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class Logo(models.Model):

    name = models.CharField(max_length = 255)
    image = models.ImageField(upload_to="rotatelogos/", max_length=255, blank=False, null=False)
    thumbnail = models.ImageField(upload_to="rotatelogos/", max_length=255, blank=True, null=True) 

    def create_thumbnail(self):

        thumb_size = (190,95)
         
        DJANGO_TYPE = self.image.file.content_type
         
        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
         
        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(StringIO(self.image.read()))
         
        image.thumbnail(thumb_size, Image.ANTIALIAS)
         
        # Save the thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)
         
        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
        temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)
         
    def save(self):
        # create a thumbnail
        self.create_thumbnail()
         
        super(Logo, self).save() 