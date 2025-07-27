from django import forms
from .models import cam

class VideoForm(forms.ModelForm):
    class Meta:
        model = cam
        fields = ['name','file']
        labels = {
            'name': '摄像头名称',
            'file': '实时视频',
        }