from django.db import models

# Create your models here.

class User(models.Model):#继承models.Model
    id = models.AutoField(primary_key=True,verbose_name="序号")
    account = models.CharField(max_length=100, verbose_name="用户名")
    password = models.CharField(max_length=100, verbose_name='密码')

    #调用类时，输出各自的属性值
    def __str__(self):
        return self.account

    class Meta:
        verbose_name = "用户"