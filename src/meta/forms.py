from django import forms
from .models import Stations

class MetaForm(forms.ModelForm):
	class Meta:
		model = Stations
		fields = ['nombre','direccion','barrio','longitud','latitud','telefono_contacto','clase']
	def __init__(self,*args,**kwargs):
		kwargs['initial']={'clase':'Section'}
		super(MetaForm,self).__init__(*args,**kwargs)
