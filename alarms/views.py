from urllib import request
from django.http import JsonResponse, HttpResponse
import json
import os
from django.core.files import File
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.views import check_login
from .models import Picture
from zipfile import ZipFile
from yolo import settings
# Create your views here.
host=[i for i in settings.ALLOWED_HOSTS]

@check_login
def pages(request):
    if request.method == 'POST':
        all_data = Picture.objects.all()
        paginator = Paginator(all_data, 3)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)
        pic_url=[]
        for i in all_data:
            pic_url.append('http://'+host[0]+'/'+'media'+'/'+i.pic_url)
        return JsonResponse({'total': paginator.count, 'current_page': page_obj.number,'url':pic_url})

@check_login
def search(request):
    if request.method == "POST":
        json_str = request.body
        json_obj = json.loads(json_str)
        channel = json_obj['pic_channel']
        s_type = json_obj['pic_type']
        time_start = json_obj['pic_time_start']
        time_end = json_obj['pic_time_end']
        the_pic = Picture.objects.filter(pic_channel=channel,pic_type=s_type,pic_time__gte=time_start,pic_time__lte=time_end)
        paginator = Paginator(the_pic, 3)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)
        pic_url = []
        for i in the_pic:
            pic_url.append('http://'+host[0]+'/'+'media'+'/'+i.pic_url)
        return JsonResponse({'total': paginator.count, 'current_page': page_obj.number, 'url': pic_url})

@check_login
def download(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    channel = json_obj['pic_channel']
    s_type = json_obj['pic_type']
    time_start = json_obj['pic_time_start']
    time_end = json_obj['pic_time_end']
    zip_filename ='导出结果'+'.zip'
    zip_file = open(zip_filename, 'w+b')
    the_pic = Picture.objects.filter(pic_channel=channel, pic_type=s_type, pic_time__gte=time_start, pic_time__lte=time_end)
    pic_url=[i.pic_url for i in the_pic]
    if not pic_url:
        result={'code':10401,'error':'照片不存在'}
        return JsonResponse(result)
    else:
        with ZipFile(zip_file, 'w') as zf:
            for filename in pic_url:
                file_path=os.path.join(settings.STATIC_URL,filename)
                zf.write(file_path,filename)
        zip_file.close()
        with open(zip_filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment;filename=download.zip'
            return response


@check_login
def delete_picture(request):
    if request.method == "DELETE":
        all_data = Picture.objects.all()
        paginator = Paginator(all_data, 3)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_pagec(page_num)
        pic_url = []
        for i in all_data:
            pic_url.append('http://'+host[0]+'/'+'media'+'/'+i.pic_url)
        return JsonResponse({'total': paginator.count, 'current_page': page_obj.number, 'url': pic_url})


