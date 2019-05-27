from .models import Basin
from rest_framework import generics, permissions, pagination
from .permissions import IsOwnerOrReadOnly
from .serializers import BasinSerializer


class BasinDetailAPIView(generics.RetrieveAPIView):
    queryset            = Basin.objects.all()
    serializer_class    = BasinSerializer
    lookup_field        = 'slug'
    permission_classes  = [IsOwnerOrReadOnly]

class BasinListAPIView(generics.ListAPIView):
    queryset            = Basin.objects.all()
    serializer_class    = BasinSerializer
    permission_classes  = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView
from django.db.models import Q
from .models import Stations
from .forms import MetaForm
from django.contrib.auth.mixins import LoginRequiredMixin

class estacionesListView(LoginRequiredMixin,ListView):
	def get_queryset(self):
		return Stations.objects.filter(clase='Section')

class estacionesDetailView(LoginRequiredMixin,DetailView):
	def get_queryset(self):
		return Stations.objects.filter(clase='Section')

class estacionesCreateView(LoginRequiredMixin,CreateView):
	form_class = MetaForm
	login_url = "/login/"
	template_name = "form.html"

	def form_valid(self,form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		SUPER = super(estacionesCreateView,self).form_valid(form)
		return SUPER

	def get_context_data(self,*args,**kwargs):
		context = super(estacionesCreateView,self).get_context_data(*args,**kwargs)
		context['title'] = 'estacion' # not necessary for now
		return context

class estacionesUpdateView(LoginRequiredMixin,UpdateView):
	form_class = MetaForm
	template_name = "meta/detail-update.html"

	def form_valid(self,form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		return super(estacionesUpdateView,self).form_valid(form)

	def get_context_data(self,*args,**kwargs):
		context = super(estacionesUpdateView,self).get_context_data(*args,**kwargs)
		context['title'] = 'Actualizar estacion: %s'%self.get_object().nombre
		return context

	def get_queryset(self):
		return Stations.objects.filter(clase='Section')

	def get_form_kwargs(self):
		kwargs = super(estacionesUpdateView,self).get_form_kwargs()
		kwargs['initial']={'clase':'Section'}
		return kwargs
