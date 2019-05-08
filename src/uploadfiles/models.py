from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from meta.models import Stations
from hidraulics.models import Item
from django.urls import reverse
import os
from uuid import uuid4

class UploadImage(models.Model):
    user                = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    company             = models.ForeignKey(Item,on_delete=models.CASCADE)
    description         = models.CharField(max_length=255, blank=True)
    document            = models.ImageField(upload_to='documents/')
    badformat           = models.CharField(max_length=255,blank=True)
    uploaded_at         = models.DateTimeField(auto_now_add=True)
    slug  				= models.SlugField(null=True,blank = True)

    def __str__(self):
    		return '%s'%(self.company)
    def get_absolute_url(self):
        print ('Gettin absolute url: user = %s' %self.user.username)
        return reverse('uploadfiles:upload',kwargs={'username':self.user.username}) #slug=self.slug

def rl_pre_save_receriver(sender,instance,*args,**kwargs):
	print('saving')
	print(instance.timestamp)
	#if not instance.slug:
#		instance.slug = unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receriver,sender = Item)
