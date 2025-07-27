from django.db import models

# Create your models here.
class Caqulate(models.Model):
    the_id = models.CharField(primary_key=True, max_length=20, unique=True)
    satuation=models.CharField(max_length=20)
    address=models.CharField(max_length=50)
    channel_name = models.CharField(max_length=50)
    update_time=models.DateTimeField(auto_now=True)
    peo_open_close=models.BooleanField(default=False)
    peo_degree=models.CharField(max_length=50,default='50')
    peo_pinglv=models.CharField(max_length=50,default='50')
    car_open_close=models.BooleanField(default=False)
    car_degree=models.CharField(max_length=50,default='50')
    car_pinglv=models.CharField(max_length=50,default='50')
    class Meta:
        db_table = 'caqulate'

