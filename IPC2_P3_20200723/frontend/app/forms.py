from django import forms

class UploadFileForm(forms.Form):
    archivo = forms.FileField()

class TestMessageForm(forms.Form):
    mensaje = forms.CharField(max_length=100)