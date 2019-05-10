from django import forms
from .models import Item,Section,Topo
import datetime
from datetimewidget.widgets import DateTimeWidget
dateTimeOptions = {	'format': 'dd/mm/yyyy HH:ii',
					'autoclose': True,
					'showMeridian' : True
					}

class ItemCreateForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = [	'item_fk','date','tipo_salida','tipo_aforo','ancho_superficial','y_lamina','x_lamina']
		labels = dict(zip(fields,[	"Estacion",'Fecha',"Tipo de campaña","Tipo de aforo",'Ancho del canal',"lamina","Sensor-x"]))
		widgets = dict(zip(['date'],[DateTimeWidget(options=dateTimeOptions)]))

	def __init__(self,user=None,*args,**kwargs):
		super(ItemCreateForm,self).__init__(*args,**kwargs)

class ItemUpdateForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['date','tipo_salida','tipo_aforo','ancho_superficial','y_lamina','x_lamina','calidad']
		labels = dict(zip(fields,["Fecha","Tipo de campaña","Tipo de aforo",'Ancho del canal',"lamina","Sensor-x","Calidad"]))
		widgets = dict(zip(['date'],[DateTimeWidget(dateTimeOptions)]))

	def __init__(self,user=None,*args,**kwargs):
		super(ItemUpdateForm,self).__init__(*args,**kwargs)

class SectionForm(forms.ModelForm):
	class Meta:
		model = Section
		fields = ['fk','vertical','x','y','v02','v04','v08','vsup']
		labels = dict(zip(fields,["aforo","Vertical","x","y",'V02','V04','V08','Vsup']))

	def __init__(self,user=None,*args,**kwargs):
		self.user = user
		last_item_instance = Item.objects.filter(user=self.user)
		last_item_instance = last_item_instance.latest('updated')
		section_objects = Section.objects.filter(fk = last_item_instance)
		count = section_objects.count()
		if count == 0.0:
			kwargs['initial']={'fk':last_item_instance.pk,'vertical':1,'x':0.0,'y':0.0}
		else:
			kwargs['initial']={'fk':last_item_instance.pk,'vertical':count+1}
		super(SectionForm,self).__init__(*args,**kwargs)

class SectionUpdateForm(forms.ModelForm):
	class Meta:
		model = Section
		fields = ['vertical','x','y','v02','v04','v08','vsup']
		labels = dict(zip(fields,["Vertical","x","y"]))

	def __init__(self,user=None,*args,**kwargs):
		super(SectionUpdateForm,self).__init__(*args,**kwargs)


class TopoForm(forms.ModelForm):
	class Meta:
		model = Topo
		fields = ['fk','vertical','x','y']
		labels = dict(zip(fields,["","Vertical","x","y"]))

	def __init__(self,user=None,*args,**kwargs):
		self.user = user
		last_item_instance = Item.objects.filter(user=self.user)
		last_item_instance = last_item_instance.latest('updated')
		section_objects = Topo.objects.filter(fk = last_item_instance)
		count = section_objects.count()
		if count == 0.0:
			kwargs['initial']={'fk':last_item_instance.pk}
		else:
			kwargs['initial']={'fk':last_item_instance.pk,'vertical':count+1}
		super(TopoForm,self).__init__(*args,**kwargs)

class TopoUpdateForm(forms.ModelForm):
	class Meta:
		model = Section
		fields = ['vertical','x','y']
		labels = dict(zip(fields,["Vertical","x","y"]))

	def __init__(self,user=None,*args,**kwargs):
		super(TopoUpdateForm,self).__init__(*args,**kwargs)
