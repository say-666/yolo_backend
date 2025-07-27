from django import forms
from img.models import img

class imgInfoForm(forms.ModelForm):
    class Meta:
        model = img
        fields = ['start_datetime','end_datetime','channel_type','alert_type','image1','image2','image3','image4','image5','image6','image7','image8']

        labels = {
            'start_datetime':'开始时间',
            'end_datetime':'结束时间',
            'channel_type':'通道类型',
            'alert_type':'告警类型',
            'image1':'图片文件',
            'image2':'图片文件',
            'image3':'图片文件',
            'image4':'图片文件',
            'image5':'图片文件',
            'image6':'图片文件',
            'image7':'图片文件',
            'image8':'图片文件',
        }