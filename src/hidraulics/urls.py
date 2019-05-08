from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from .views import *

urlpatterns = [
	url(r'^nuevo-item/$', ItemCreateView.as_view(),name='nuevo-item'),
	url(r'^item/(?P<pk>\d+)/$', ItemUpdateView.as_view(),name = 'item'),
	url(r'^vertical/(?P<pk>\d+)/$', SectionUpdateView.as_view(),name = 'vertical'),
	url(r'^nueva-vertical/$', SectionCreateView.as_view(),name = 'nueva-vertical'),
	url(r'^borrar-vertical/(?P<pk>\d+)/$', delete_section,name = 'borrar-vertical'),
	url(r'^topobatimetria/(?P<pk>\d+)/$', TopoUpdateView.as_view(),name = 'topo'),
	url(r'^nueva-topobatimetria/$', TopoCreateView.as_view(),name = 'nueva-topo'),
	url(r'^borrar-topobatimetria/(?P<pk>\d+)/$', delete_topo,name = 'borrar-topo'),
	url(r'^transferir-topobatimetria/(?P<pk>\d+)/$', transfer_to_topo,name = 'transferir-topo'),
]
