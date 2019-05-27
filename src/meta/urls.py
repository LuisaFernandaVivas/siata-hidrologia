from django.urls import path, re_path
from django.conf.urls import url
from .views import (
        BasinDetailAPIView,
        BasinListAPIView,
    	estacionesListView,
    	estacionesCreateView,
    	estacionesDetailView,
    	estacionesUpdateView
    )

app_name = 'basin-api'
urlpatterns = [
    path(r'api/basin/', BasinListAPIView.as_view(), name='basin-list'),
    re_path(r'api/basin/(?P<slug>[\w-]+)/$', BasinDetailAPIView.as_view(), name='basin-detail'),
    url(r'^gauge-stations/nuevo/$', estacionesCreateView.as_view(),name='nuevo'),
    url(r'^gauge-stations/(?P<slug>[\w-]+)/$', estacionesUpdateView.as_view(),name = 'detalle'),
]
