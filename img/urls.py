from django.urls import path
from . import views

urlpatterns = [
    path('upload_img', views.upload_img, name='上传图片数据'),
    path('query_img',views.query_img,name='查询图片数据'),
    path('delete_Recording',views.delete_Recording,name='删除图片记录'),
    path('download_filtered_images_zip',views.download_filtered_images_zip,name="导出并下载查询图片的zip包"),
    ]