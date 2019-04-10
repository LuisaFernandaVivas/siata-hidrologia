"""reactify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include, re_path
from django.conf.urls import url

def send_file(request):

  import os, tempfile, zipfile
  from wsgiref.util import FileWrapper
  from django.conf import settings
  import mimetypes

  filename     = "C:\ex2.csv" # Select your file here.
  download_name ="data.csv"
  wrapper      = FileWrapper(open(filename))
  content_type = mimetypes.guess_type(filename)[0]
  response     = HttpResponse(wrapper,content_type=content_type)
  response['Content-Length']      = os.path.getsize(filename)
  response['Content-Disposition'] = "attachment; filename=%s"%download_name
  return response



urlpatterns = [
    path('', TemplateView.as_view(template_name='react.html')),
    path('walking', TemplateView.as_view(template_name='walking.html')),
    re_path(r'^posts/', TemplateView.as_view(template_name='react.html')),
    path('admin/', admin.site.urls),
    path('api/posts/', include('posts.urls')),
    path('api/basin/', include('meta.urls')),
    path('static/data.csv', send_file)
]
