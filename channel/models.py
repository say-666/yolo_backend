from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

# 通道管理
class channel(models.Model):
    # 序号
    id = models.AutoField(primary_key=True, verbose_name="序号")
    # 通道状态
    STATUS_CHOICES = [
        ('Not configured', '未配置'),
        ('online', '在线'),
        ('offline', '离线'),
    ]
    status = models.CharField(max_length=120,
                              choices=STATUS_CHOICES,
                              default='未配置',
                              verbose_name='通道状态')
    # RTSP地址
    rtsp_url = models.CharField(max_length=255,default='rtsp://xxxx', verbose_name="RTSP地址")
    # 通道名称
    channel_name = models.CharField(max_length=255, verbose_name="通道名称")
    # 周界
    perimeter = models.CharField(max_length=255, null=True, verbose_name="周界")
    # 修改时间
    updatetime = models.TimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        verbose_name = "通道管理"
        verbose_name_plural = "通道管理"

# 算法配置
class algorithm(models.Model):
    # 告警类型
    ALERT_TYPE_CHOICES = [
        ('people_count', '人数统计'),
        ('vehicle_count', '车辆统计'),
    ]
    car_alert_type = models.CharField(max_length=15, choices=ALERT_TYPE_CHOICES, verbose_name="告警类型")
    human_alert_type = models.CharField(max_length=15, choices=ALERT_TYPE_CHOICES, verbose_name="告警类型")

    # 开关状态
    SWITCH_CHOICES = [
        ('off', '关'),
        ('on', '开'),
    ]

    human_switch_status = models.CharField(
        max_length=20,
        choices=SWITCH_CHOICES,
        default='off',
        verbose_name="开关状态"
    )
    car_switch_status = models.CharField(
        max_length=20,
        choices=SWITCH_CHOICES,
        default='off',
        verbose_name="开关状态"
    )
    # 灵敏度
    human_sensitivity = models.IntegerField(
        default=60,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="灵敏度"
    )
    car_sensitivity = models.IntegerField(
        default=60,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="灵敏度"
    )
    # 上报频率(秒)
    human_report_frequency = models.IntegerField(
        default=5,
        verbose_name="上报频率(秒)"
    )
    car_report_frequency = models.IntegerField(
        default=5,
        verbose_name="上报频率(秒)"
    )
    # 修改时间
    updatetime = models.TimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        verbose_name = "算法配置"
        verbose_name_plural = "算法配置"