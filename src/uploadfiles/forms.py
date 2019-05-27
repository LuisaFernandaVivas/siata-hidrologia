from django import forms
from .models import UploadImage

class UploadFilesForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ('company','description', 'document', )
        labels = dict(zip(fields,["Registro","Descripción","Foto"] ) )
