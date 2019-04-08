from django.urls import path, re_path

from .views import (
        BasinDetailAPIView,
        BasinListAPIView,
    )

app_name = 'basin-api'
urlpatterns = [
    path('', BasinListAPIView.as_view(), name='basin-list'),
    re_path(r'^(?P<slug>[\w-]+)/$', BasinDetailAPIView.as_view(), name='basin-detail'),
]
