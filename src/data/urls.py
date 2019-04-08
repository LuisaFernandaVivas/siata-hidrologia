from django.urls import path, re_path

from django.conf.urls import url

from .views import (
        DataBasinDetailAPIView,
        DataBasinListAPIView,
    )

app_name = 'data-api'
urlpatterns = [
    url(r'^basin/$', DataBasinListAPIView.as_view(), name='basin-list'),
    url(r'^basin/(?P<pk>\d+)/$', DataBasinListAPIView.as_view(), name='basin-detail'),
]
