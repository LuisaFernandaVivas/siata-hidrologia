from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .forms import UploadFilesForm
from .models import UploadImage

sdb = settings.DATABASES['default']

class UploadFilesView(LoginRequiredMixin,CreateView):
    form_class      = UploadFilesForm
    template_name   = "uploadfiles/upload.html"

    def form_valid(self,form,**kwargs):
        ''' requires form to..'''
        instance        = form.save(commit=False)
        instance.user   = self.request.user
        SUPER           = super(UploadFilesView,self).form_valid(form)
        print ('UFV:form_valid:form:%s'%form)
        return SUPER
