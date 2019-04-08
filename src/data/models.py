from django.db import models
from meta.models import Basin
from django.conf import settings

class DataBasin(models.Model):
	fk   							= models.ForeignKey(Basin,on_delete=models.CASCADE)
	date							= models.DateTimeField(null = False,blank = False)
	water_level           			= models.FloatField(null = True,blank = True)
	sensor_level           			= models.FloatField(null = True,blank = True)
	radar_rain			            = models.FloatField(null = True,blank = True)
	interpolated_rain               = models.FloatField(null = True,blank = True)
	water_flow                 		= models.FloatField(null = True,blank = True)
	section_area                 	= models.FloatField(null = True,blank = True)
	water_surface_velocity       	= models.FloatField(null = True,blank = True)
	water_level_color               = models.CharField(max_length = 120,null = True,blank = True)
	radar_rain_color				= models.CharField(max_length = 120,null = True,blank = True)
	water_surface_velocity_color   	= models.CharField(max_length = 120,null = True,blank = True)
	interpolated_rain_color     	= models.CharField(max_length = 120,null = True,blank = True)
	updated							= models.DateTimeField(auto_now=True)
	timestamp						= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '%s'%(self.date.strftime('%Y-%m-%d %H:%M'))
	class Meta:
		ordering = ['-updated','-timestamp']
