from datetime import datetime
from urllib import request
from .models import Caqulate
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.views import View
from user.views import check_login
# Create your views here.
@check_login
def caqulate_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        the_id = data['the_id']
        address = data['address']
        channel_name = data['channel_name']
        update_time=datetime.now()
        popen_close = data['peo_open_close']
        pdegree = data['peo_degree']
        ppinglv = data['peo_pinglv']
        copen_close = data['car_open_close']
        cdegree = data['car_degree']
        cpinglv = data['car_pinglv']
        if popen_close==False and copen_close==False:
            satuation='离线'
        else:
            satuation='在线'
        try:
            the_caqulate=Caqulate.objects.get(the_id=the_id)
        except Exception as e:
            result={'code':10301,'error':'没有该配置'}
            return JsonResponse(result)
        the_caqulate.address=address
        the_caqulate.channel_name=channel_name
        the_caqulate.update_time=update_time
        the_caqulate.satuation=satuation
        the_caqulate.peo_open_close = popen_close
        the_caqulate.peo_degree = pdegree
        the_caqulate.peo_pinglv = ppinglv
        the_caqulate.car_open_close = copen_close
        the_caqulate.car_degree = cdegree
        the_caqulate.car_pinglv = cpinglv
        the_caqulate.save()
        resutl = {"code": 200, 'msg': "ok"}
        return JsonResponse(resutl)


@check_login
def caqulate_detail(request):
    if request.method == "POST":
        json_str = request.body
        json_obj = json.loads(json_str)
        the_id = json_obj['the_id']
        try:
            data = Caqulate.objects.get(the_id=the_id)
        except Exception as e:
            result={'code':'10302','error':'配置不存在'}
            return JsonResponse(result)
        the_id = data.the_id
        channel_name = data.channel_name
        address = data.address
        popen_close = data.peo_open_close
        copen_close = data.car_open_close
        pdegree=data.peo_degree
        ppinglv=data.peo_pinglv
        cdegree=data.car_degree
        cpinglv=data.car_pinglv
        update_time=data.update_time
        if popen_close==False and copen_close==False:
            satuation='离线'
        else:
            satuation='在线'
        data.satuation=satuation
        data.save()
        back={'the_id':the_id,'satuation':satuation,'address':address,'channel_name':channel_name,'popen_close':popen_close,'copen_close':copen_close,'pdegree':pdegree,'ppinglv':ppinglv,'cdegree':cdegree,'cpinglv':cpinglv,'update_time':update_time}
        return JsonResponse({'code':200,"data":back})

@check_login
def restart_channel(request):
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        the_id = json_obj['the_id']
        try:
            data = Caqulate.objects.get(the_id=the_id)
        except Exception as e:
            result={'code':10303,'error':'未找到该配置'}
            return JsonResponse(result)
        data.satuation='离线'
        data.peo_open_close = False
        data.car_open_close = False
        data.update_time=datetime.now()
        data.save()
        resutl={"code":200,"msg":"ok"}
        return JsonResponse(resutl)

@check_login
def restart_setting(request):
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        the_id = json_obj['the_id']
        try:
            data = Caqulate.objects.get(the_id=the_id)
        except Exception as e:
            result = {'code': 10304, 'error': '未找到该配置'}
            return JsonResponse(result)
        data.peo_open_close=False
        data.peo_degree=50
        data.peo_pinglv=5
        data.car_open_close=False
        data.car_degree=50
        data.car_pinglv=5
        data.update_time=datetime.now()
        data.satuation='离线'
        data.save()
        resutl={"code":200,'msg':"ok"}
        return JsonResponse(resutl)

@check_login
def simulate_caqulate(request):
    my_id=[1,2,3,4]
    if request.method == "POST":
        json_str = request.body
        json_obj = json.loads(json_str)
        the_id = json_obj['the_id']
        try:
            data = Caqulate.objects.get(the_id=the_id)
        except Exception as e:
            result={'code':10305,'error':'未找到该配置'}
            return JsonResponse(result)
        popen_close = data.peo_open_close
        copen_close = data.car_open_close
        pdegree = data.peo_degree
        ppinglv = data.peo_pinglv
        cdegree = data.car_degree
        cpinglv = data.car_pinglv
        update_time = datetime.now()
        for i in my_id:
            if i !=the_id:
                t_data=Caqulate.objects.get(the_id=i)
                t_data.update_time=update_time
                t_data.car_open_close=copen_close
                t_data.car_degree=cpinglv
                t_data.car_pinglv=ppinglv
                t_data.peo_open_close=popen_close
                t_data.peo_degree=pdegree
                t_data.peo_pinglv=ppinglv
                t_data.save()
        resutl={"code":200,'msg':"ok"}
        return JsonResponse(resutl)