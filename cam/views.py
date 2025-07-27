from urllib import request

from django.core.files.storage import default_storage
from django.urls import NoReverseMatch

from Users.views import login_required
from Yolo import settings
from channel.models import channel, algorithm
from img.models import img
from .forms import VideoForm
from django.http import JsonResponse
from .models import cam
from rest_framework import serializers

class camsserializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class channelsserializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.CharField()
# 获取列表数据
@login_required
def get_form(request):
    try:
        cam_to_get = cam.objects.all()
    except cam.DoesNotExist:
        return JsonResponse({'code': 11501, 'msg': '摄像头数据不存在'})
    cams=camsserializer(instance=cam_to_get,many=True)
    cams_data=cams.data
    # file_ =  str(cam_to_get.file)
    # video_f_url = request.build_absolute_uri(settings.MEDIA_URL + file_)
    try:
        channel_to_get = channel.objects.all()
    except channel.DoesNotExist:
        return JsonResponse({'code': 11503, 'msg': '通道数据不存在'})
    channels=channelsserializer(instance=channel_to_get,many=True)
    channels_data=channels.data
    # 使用字典解包来合并两个序列化后的数据
    return JsonResponse({"code": 200, "msg": "获取成功", "cams_data": cams_data,"channels_data":channels_data})

class imgsserializer(serializers.Serializer):
    id = serializers.IntegerField()
    image1 = serializers.FileField()
    image2 = serializers.FileField()
    image3 = serializers.FileField()
    image4 = serializers.FileField()
    image5 = serializers.FileField()
    image6 = serializers.FileField()
    image7 = serializers.FileField()
    image8 = serializers.FileField()

    def get_image_url(self, obj, field_name):
        request = self.context.get('request')
        if getattr(obj, field_name):
            file_url = getattr(obj, field_name).url
            return request.build_absolute_uri(file_url)
        return None

    def get_image1(self, obj):
        return self.get_image_url(obj, 'image1')

    def get_image2(self, obj):
        return self.get_image_url(obj, 'image2')

    def get_image3(self, obj):
        return self.get_image_url(obj, 'image3')

    def get_image4(self, obj):
        return self.get_image_url(obj, 'image4')

    def get_image5(self, obj):
        return self.get_image_url(obj, 'image5')

    def get_image6(self, obj):
        return self.get_image_url(obj, 'image6')

    def get_image7(self, obj):
        return self.get_image_url(obj, 'image7')

    def get_image8(self, obj):
        return self.get_image_url(obj, 'image8')

#获取图片数据
def get_img(request):
    try:
        imgs_to_get = img.objects.all()
    except img.DoesNotExist:
        return JsonResponse({'code': 11502, 'msg': '图片数据不存在'})
    imgs=imgsserializer(instance=imgs_to_get,many=True,context={'request': request})
    imgs_data=imgs.data
    return JsonResponse({"code": 200, "msg": "获取成功", "imgs_data": imgs_data})

class videosserializer(serializers.Serializer):
    id = serializers.IntegerField()
    file = serializers.FileField()

    def get_file(self, obj):
        # 获取文件的完整 URL
        if obj.file:
            try:
                # 尝试获取文件的 URL
                return request.build_absolute_uri(obj.file.url)
            except NoReverseMatch:
                # 如果没有为文件字段定义 URL，使用 MEDIA_URL 拼接
                return request.build_absolute_uri(settings.MEDIA_URL + obj.file.name)
        return None

#获取视频数据
def get_video(request):
    try:
        cams_to_get = cam.objects.all()
    except cam.DoesNotExist:
        return JsonResponse({'code': 11501, 'msg': '摄像头数据不存在'})
    cams=videosserializer(instance=cams_to_get,many=True,context={'request': request})
    cams_data=cams.data
    return JsonResponse({"code":200,"msg":"获取成功","camera_info":cams_data})

class algorithmsserializer(serializers.Serializer):
    id = serializers.IntegerField()
    car_alert_type=serializers.CharField()
    human_alert_type=serializers.CharField()
    human_switch_status=serializers.CharField()
    car_switch_status=serializers.CharField()
    car_sensitivity=serializers.CharField()
    human_sensitivity=serializers.CharField()
    human_report_frequency=serializers.CharField()
    car_report_frequency=serializers.CharField()

class channelserializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.CharField()
    rtsp_url = serializers.CharField()
    channel_name = serializers.CharField()


#获取详细信息
def get_detailedform(request):
    try:
        channel_to_get = channel.objects.all()
    except channel.DoesNotExist:
        return JsonResponse({'code': 11503, 'msg': '通道数据不存在'})
    channels=channelserializer(instance=channel_to_get,many=True)
    channels_data=channels.data
    try:
        algorithm_to_get = algorithm.objects.all()
    except algorithm.DoesNotExist:
        return JsonResponse({'code': 11504, 'msg': '算法配置数据不存在'})
    algorithms=algorithmsserializer(instance=algorithm_to_get,many=True)
    algorithms_data=algorithms.data
    return JsonResponse({"code":200,"msg":"获取成功","channels_data":channels_data,"algorithms_data":algorithms_data})


# 新增摄像头数据
@login_required
def add_camera(request):
    form = VideoForm(request.POST, request.FILES)
    # 当表单数据存在时
    if form.is_valid():
        form.save()
        return JsonResponse({'code': 200, 'msg': '新增摄像头数据成功'})
    else:
        # 表单数据无效时返回错误信息
        return JsonResponse({'code': 11505, 'msg': '表单数据无效'})


# 删除摄像头(数据库记录，不会删除视频信息)
@login_required
def delete_camera(request):
    try:
        cam_id = request.GET.get('id')
        if not cam_id:
            return JsonResponse({'code': 11506, 'msg': '摄像头ID不能为空'})
        # 获取通道对象
        cam_obj = cam.objects.get(id=cam_id,is_active=True)
    except cam.DoesNotExist:
        return JsonResponse({'code': 11507, 'msg': '摄像头数据不存在'})
    except Exception as e:
        return JsonResponse({'code': 11508, 'msg': '服务器内部错误'})

    # #删除文件(可实现删除上传的视频数据而不是视频数据在数据库的记录)(选用)
    # absolute_ = cam_obj.file.
    # os.remove(absolute_)

    cam_obj.is_active = False
    cam_obj.save()
    return JsonResponse({'code': 200, 'msg': '删除摄像头成功'})