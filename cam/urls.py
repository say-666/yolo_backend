from django.urls import path

from . import views

urlpatterns = [
    path('add_camera', views.add_camera, name='增加摄像头'),
    path('delete_camera', views.delete_camera, name='删除摄像头'),
    path('get_video',views.get_video,name='获取视频数据'),
    path('get_detailedform',views.get_detailedform,name='获取列表详细数据'),
    path('get_img',views.get_img,name='获取图片数据'),
    path('get_form',views.get_form,name='获取列表数据'),
]