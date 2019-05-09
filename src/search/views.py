from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render,get_object_or_404
from django.views.generic import DetailView,CreateView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.http import Http404
from meta.models import Stations
from hidraulics.models import Item
from django.db.models import Q

import locale
locale.setlocale( locale.LC_ALL, '' )
User = get_user_model()

def search(self,query):
	if query:
		query = query.strip()
		filtro =  self.filter(
			Q(nombre__icontains=query)|
			Q(nombre__iexact=query)
			).distinct()
		return filtro
	else:
		return self.none()

class ProfileDetailView(LoginRequiredMixin,DetailView):
	template_name = 'user.html'

	def get_object(self):
		if self.kwargs.get("username") is None :
			raise Http404
		return get_object_or_404(User,username__iexact=self.kwargs.get("username"),is_active=True)

	def get_context_data(self,*args,**kwargs):
		context = super(ProfileDetailView,self).get_context_data(*args,**kwargs)
		query = self.request.GET.get('q')
		items_exists = Item.objects.all().exists() # todos los objetos
		qs = Stations.objects.filter(clase='Section')
		qs = search(qs,query)
		print('this is the query %s'%query)
		for item_obj in qs:
			item_obj.objetos = item_obj.item_set.all()
		if items_exists and qs.exists():
			context['locations'] = qs
		return context

class HomeView(LoginRequiredMixin,TemplateView):
	template_name = 'home.html'
