from django.db import models

# Create your models here.
class Picture(models.Model):
    pic_url = models.CharField(max_length=300,default=0)
    pic_name = models.CharField(max_length=300,default=0)
    pic_time = models.DateTimeField(max_length=300,default=0)
    pic_channel = models.CharField(max_length=50,default=0)
    pic_type = models.CharField(max_length=50,default=0)
    class Meta:
        db_table = 'picture'

