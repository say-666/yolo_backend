from django.db import models

# Create your models here.
class img(models.Model):
    #序号
    id = models.AutoField(primary_key=True)

    # 开始时间
    start_datetime = models.DateTimeField(verbose_name="开始时间")

    # 结束时间
    end_datetime = models.DateTimeField(verbose_name="结束时间")

    # 通道类型
    channel_type= models.CharField(max_length=255,verbose_name='通道类型')

    # 告警类型
    alert_type = models.CharField(max_length=255,verbose_name='告警类型')

    # 图片
    image1 = models.ImageField(upload_to='image',null=True,blank=True)
    image2 = models.ImageField(upload_to='image',null=True,blank=True)
    image3 = models.ImageField(upload_to='image',null=True,blank=True)
    image4 = models.ImageField(upload_to='image',null=True,blank=True)
    image5 = models.ImageField(upload_to='image',null=True,blank=True)
    image6 = models.ImageField(upload_to='image',null=True,blank=True)
    image7 = models.ImageField(upload_to='image',null=True,blank=True)
    image8 = models.ImageField(upload_to='image',null=True,blank=True)

