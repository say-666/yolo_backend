# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class cam(models.Model):

    #摄像头序号
    id = models.AutoField(primary_key=True, verbose_name="序号")

    # 摄像头名称
    name = models.CharField(max_length=50, verbose_name="摄像头名称")

    # 修改时间
    updatetime = models.TimeField(verbose_name="修改时间", auto_now=True)

    # 实时视频
    file = models.FileField(upload_to='videos')

    class Meta:
        verbose_name = "摄像头"
        verbose_name_plural = "摄像头"  # 设置复数名称

