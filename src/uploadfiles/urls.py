from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .views import 	UploadFilesView

urlpatterns = [
    url(r'(?P<username>[\w-]+)/$', UploadFilesView.as_view(),name='upload')
    ]
