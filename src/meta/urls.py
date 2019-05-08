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
    path('', BasinListAPIView.as_view(), name='basin-list'),
    re_path(r'^(?P<slug>[\w-]+)/$', BasinDetailAPIView.as_view(), name='basin-detail'),
    url(r'^nuevo/$', estacionesCreateView.as_view(),name='nuevo'),
    url(r'^gauge-station/(?P<slug>[\w-]+)/$', estacionesUpdateView.as_view(),name = 'detalle'),
]
