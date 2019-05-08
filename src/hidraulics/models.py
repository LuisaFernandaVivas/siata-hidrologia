from django.conf import settings
from django.db import models
from django.utils import timezone
from meta.models import *
from django.urls import reverse
import datetime
import pandas as pd

class Item(models.Model):
	user 							= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	item_fk							= models.ForeignKey(Stations,on_delete=models.CASCADE)
	aforo							= models.CharField(max_length = 15, null = True,blank = True)
	fecha							= models.DateField(null = True,blank = True)
	date     						= models.DateTimeField(null = True,blank = True)
	calidad                         = models.IntegerField(null = True,blank=True,choices =((0,'mala'),(1,'buena'),(2,'sin calificar')))
	hora 							= models.IntegerField(null=True,blank = True,choices = tuple(zip(range(24),range(24))))
	minuto 							= models.IntegerField(null=True,blank = True,choices =tuple(zip(range(60),range(60))))
	aforo							= models.IntegerField(null = True,blank = True)
	x_lamina						= models.FloatField(null = True,blank = True)
	y_lamina						= models.FloatField(null = True,blank = True)
	tipo_salida						= models.CharField(max_length=30,choices = (('redrio-rio', 'Redrio-Río'),	('redrio-quebradas', 'Redrio-Queb'), ('redrio-modelacion',u'Redrío-Model'),('siata-aforo',u'Siata Aforo'),('siata-batimetria',u'Siata-topo'),('siata-completo',u'Siata-Completo'),),null=True,blank=True)
	tramo							= models.IntegerField(null = True,blank = True)
	codigo_sensor_nivel 			= models.IntegerField(null = True,blank = True)
	codigo_sensor_vel_sup			= models.IntegerField(null = True,blank = True)
	tipo_aforo						= models.CharField(max_length=50,choices = (('vadeo', 'Vadeo'),('suspencion', 'Suspención'),('curva calibracion','Curva de calibración'),('diferencia','Diferencia')),null=True,blank=True)
	caudal_total					= models.FloatField(null = True,blank = True)
	error_caudal					= models.FloatField(null = True,blank = True)
	area_mojada						= models.FloatField(null = True,blank = True)
	profundidad_media 				= models.FloatField(null = True,blank = True)
	perimetro_mojado 				= models.FloatField(null = True,blank = True)
	dispositivo 					= models.CharField(max_length = 15, default='MF-PRO',null = True,blank = True)
	error_dispositivo				= models.FloatField(null = True,blank = True)
	ancho_superficial				= models.FloatField(null = True,blank = True)
	velocidad_promedio				= models.FloatField(null = True,blank = True)
	radio_hidraulico 				= models.FloatField(null = True,blank = True)
	longitud 						= models.FloatField(null = True,blank = True)
	latitud 						= models.FloatField(null = True,blank = True)
	texto_1 						= models.TextField(null=True,blank=True)
	texto_2							= models.TextField(null=True,blank=True)
	timestamp						= models.DateTimeField(auto_now_add=True)
	updated							= models.DateTimeField(auto_now=True)
	offset                          = models.FloatField(null=True,blank=True)
	def __str__(self):
		return '%s-%s'%(self.item_fk,self.date.strftime("%Y%m%d%H%M"))

	def get_absolute_url(self):
		return reverse('hidraulics:item',kwargs = {'pk':self.pk})

	class Meta:
		ordering = ['-updated','-timestamp']

class Section(models.Model):
	user 							= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	fk	    						= models.ForeignKey(Item,on_delete=models.CASCADE)
	vertical                        = models.IntegerField(null = True,blank = True)
	x	          					= models.FloatField(null = True,blank = True)
	y	          					= models.FloatField(null = True,blank = True)
	v01	          					= models.FloatField(null = True,blank = True)
	v02	          					= models.FloatField(null = True,blank = True)
	v03	          					= models.FloatField(null = True,blank = True)
	v04	          					= models.FloatField(null = True,blank = True)
	v05	          					= models.FloatField(null = True,blank = True)
	v06	          					= models.FloatField(null = True,blank = True)
	v07	          					= models.FloatField(null = True,blank = True)
	v08	          					= models.FloatField(null = True,blank = True)
	v09	          					= models.FloatField(null = True,blank = True)
	vsup	          				= models.FloatField(null = True,blank = True)
	vm	          					= models.FloatField(null = True,blank = True)
	area_i         					= models.FloatField(null = True,blank = True)
	caudal_i       					= models.FloatField(null = True,blank = True)
	perimetro_i                     = models.FloatField(null = True,blank = True)
	timestamp						= models.DateTimeField(auto_now_add=True)
	updated							= models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s'%(self.fk)

	def get_absolute_url(self):
		return reverse('hidraulics:vertical',kwargs = {'pk':self.pk})

	class Meta:
		ordering = ['-updated','-timestamp']


class Topo(models.Model):
	user 							= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	fk	    						= models.ForeignKey(Item,on_delete=models.CASCADE)
	vertical                        = models.IntegerField(null = True,blank = True)
	x	          					= models.FloatField(null = True,blank = True)
	y	          					= models.FloatField(null = True,blank = True)
	timestamp						= models.DateTimeField(auto_now_add=True)
	updated							= models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s'%(self.fk)

	def get_absolute_url(self):
		return reverse('hidraulics:topo',kwargs = {'pk':self.pk})

	class Meta:
		ordering = ['-updated','-timestamp']
