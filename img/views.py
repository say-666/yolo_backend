import os
import zipfile
from datetime import datetime
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from Yolo import settings
from .models import img
from Users.views import login_required
from img.forms import imgInfoForm
import pytz
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


#新增图片数据
@login_required
def upload_img(request):
    form = imgInfoForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return JsonResponse({'code': 200, 'msg': '新增图片数据成功'})
    else:
        return JsonResponse({'code': 11601, 'msg': '表单数据无效'})

#查询图片数据
@login_required
def query_img(request):
    user_start_datetime = request.GET.get('start_datetime')
    user_end_datetime = request.GET.get('end_datetime')
    user_channel_type = request.GET.get('channel_type')
    user_alert_type = request.GET.get('alert_type')

    if not user_channel_type:
        return JsonResponse({'code': 11602, 'msg': '通道类型不能为空'})
    if not user_alert_type:
        return JsonResponse({'code': 11603, 'msg': '告警类型不能为空'})
    if not user_start_datetime:
        return JsonResponse({'code': 11613, 'msg': '开始时间不能为空'})
    if not user_end_datetime:
        return JsonResponse({'code': 11605, 'msg': '结束时间不能为空'})

    try:
        start_datetime_naive = datetime.strptime(user_start_datetime, '%Y-%m-%d %H:%M:%S')
        shanghai_tz = pytz.timezone('Asia/Shanghai')
        start_datetime = shanghai_tz.localize(start_datetime_naive)
    except ValueError as e:
        return JsonResponse({'code': 11614, 'msg': '开始时间格式不正确'})

    try:
        end_datetime_naive = datetime.strptime(user_end_datetime, '%Y-%m-%d %H:%M:%S')
        shanghai_tz = pytz.timezone('Asia/Shanghai')
        end_datetime = shanghai_tz.localize(end_datetime_naive)
    except ValueError as e:
        return JsonResponse({'code': 11615, 'msg': '结束时间格式不正确'})

    if start_datetime > end_datetime:
        return JsonResponse({'code': 11606, 'msg': '开始时间不能大于结束时间'})

    images = img.objects.filter(
        start_datetime__gte=start_datetime,
        end_datetime__lte=end_datetime,
        channel_type=user_channel_type,
        alert_type=user_alert_type
    )

    keys = ['image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8']
    data = list(images.values(*keys))#把地址序列化
    f_urls = []
    for item in data:
        for key, value in item.items():
            if value:
                file_path = value
                f_url = request.build_absolute_uri(settings.MEDIA_URL + file_path)
                f_urls.append(f_url)

    items_per_page = 4  # 一个页面设四个数据
    paginator = Paginator(f_urls, items_per_page)
    current_page = request.GET.get("page", 1)

    if paginator.num_pages > 10:  # 当页数大于10时
        if current_page - 5 < 1:  # 开始的十个页面
            pageRange = range(1, 11)
        elif current_page + 5 > paginator.num_pages:  # 最后的十个页面
            pageRange = range(current_page - 5, paginator.num_pages + 1)
        else:  # 在中间的页面中
            pageRange = range(current_page - 5, current_page + 6)
    else:
        pageRange = paginator.page_range

    try:
        f_urls = paginator.page(current_page)
    except PageNotAnInteger:
        f_urls = paginator.page(1)
    except EmptyPage:
        f_urls = paginator.page(paginator.num_pages)

        # 提取分页信息
    page_info = {
        'current_page': f_urls.number,
        'num_pages': paginator.num_pages,
        'has_next': f_urls.has_next(),
        'has_previous': f_urls.has_previous(),
        'start_index': f_urls.start_index(),
        'end_index': f_urls.end_index(),
    }

    # 提取分页数据，进行序列化
    f_urls = list(f_urls)
    page_range= list(pageRange)

    if not data:
        return JsonResponse({'code': 11607, 'msg': '没有查询到任何图片数据'})
    else:
        return JsonResponse({
            'code': 200,
            'msg': '查询图片成功',
            'f_urls': f_urls,
            'page_info': page_info,
            'page_range': page_range,
        })


# 删除图片查询记录
@login_required
def delete_Recording(request):
    try:
        img_id = request.GET.get('id')
        if not img_id:
            return JsonResponse({'code': 11609, 'msg': '摄像头ID不能为空'})
        # 获取通道对象
        img_obj = img.objects.get(id=img_id)
    except img.DoesNotExist:
        return JsonResponse({'code': 11610, 'msg': '图片数据不存在'})

    # # 删除文件(可实现删除查询到的图片数据而不是图片查询记录)(选用)
    # absolute_path = img_obj.image.path
    # os.remove(absolute_path)

    # 删除数据库记录
    img_obj.is_active = False
    img_obj.save()

    return JsonResponse({'code': 200, 'msg': '图片数据删除成功'})

# 打包为zip导出
@login_required
def download_filtered_images_zip(request):
        user_start_datetime = request.GET.get('start_datetime')
        user_end_datetime = request.GET.get('end_datetime')
        user_channel_type = request.GET.get('channel_type')
        user_alert_type = request.GET.get('alert_type')
        output_filename = 'filtered_images.zip'

    # try:
        if not user_channel_type:
            return JsonResponse({'code': 11611, 'msg': '通道类型不能为空'})
        if not user_alert_type:
            return JsonResponse({'code': 11612, 'msg': '告警类型不能为空'})

        # 尝试将字符串转换为日期时间对象，并使其成为时区感知的
        if user_start_datetime:
            start_datetime_naive = datetime.strptime(user_start_datetime, '%Y-%m-%d %H:%M:%S')
            shanghai_tz = pytz.timezone('Asia/Shanghai')
            start_datetime = shanghai_tz.localize(start_datetime_naive)
        else:
            return JsonResponse({'code': 11613, 'msg': '开始时间不能为空'})

        if user_end_datetime:
            end_datatime_naive = datetime.strptime(user_end_datetime, '%Y-%m-%d %H:%M:%S')
            shanghai_tz = pytz.timezone('Asia/Shanghai')
            end_datetime = shanghai_tz.localize(end_datatime_naive)
        else:
            return JsonResponse({'code': 11614, 'msg': '结束时间不能为空'})

        if start_datetime > end_datetime:
            return JsonResponse({'code': 11615, 'msg': '开始时间不能大于结束时间'})

        else:
            images = img.objects.filter(
                start_datetime__gte=start_datetime,
                end_datetime__lte=end_datetime,
                channel_type=user_channel_type,
                alert_type=user_alert_type
            )

            if not images.exists():
                return JsonResponse({'code': 11616, 'msg': '没有找到符合条件的图片'})

            # 创建一个HttpResponse对象，用来下载文件
            response = HttpResponse(content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{output_filename}"'

            # 创建ZIP文件并写入HttpResponse对象
            with zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for image in images:
                    for i in range(1, 8):
                        image_attr = f'image{i}'
                        if hasattr(image, image_attr) and getattr(image, image_attr):
                            image_path = default_storage.path(getattr(image, image_attr).name)
                            in_zip_path = f"{image_attr}_{os.path.basename(image_path)}"
                            zipf.write(image_path, in_zip_path)
            return response
    #
    # except Exception as e:
    #     # 其他错误
    #     return JsonResponse({'code': 11617, 'msg': '服务器内部错误'})