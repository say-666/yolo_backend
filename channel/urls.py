from django.urls import path
from . import views


urlpatterns = [
    path('add_channel',views.add_channel , name='新增通道'),
    path('add_algorithm', views.add_algorithm,name='新增算法配置'),
    path('update_channel',views.update_channel ,name='修改通道信息'),
    path('update_algorithm',views.update_algorithm ,name='修改算法配置'),
    path('reboot_channel',views.reboot_channel,name='重启通道'),
    path('reset_algorithm',views.reset_algorithm,name='重置算法配置'),
    path('reset_all_algorithm',views.reset_all_algorithm,name='重置配置到所有'),
    path('delete_channel',views.delete_channel,name='删除通道数据'),
    path('delete_algorithm',views.delete_algorithm,name='删除算法配置'),
    path('get_channel',views.get_channel,name='获取通道数据'),
    path('get_algorithm',views.get_algorithm,name='获取算法配置')
]