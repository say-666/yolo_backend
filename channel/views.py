import json
from django.http import JsonResponse
from Users.views import login_required
from channel.models import algorithm
from .models import channel

# 获取通道数据
@login_required
def get_channel(request):
    try:
        #使用orm获取所有摄像头数据(返回一个字典)
        obj_cam = channel.objects.all().values()
        #把结果转化为list类型
        channels = list(obj_cam)
        return JsonResponse({"code":200,"msg":"获取成功","data":channels})
    except Exception as e:
        #如果出现异常，返回
        return JsonResponse({"code":11436,"msg":str(e)})

# 获取算法配置数据
@login_required
def get_algorithm(request):
    try:
        obj_alg = algorithm.objects.all().values()
        algorithms = list(obj_alg)
        return JsonResponse({"code":200,"msg":"获取成功","data":algorithms})
    except Exception as e:
        return JsonResponse({"code":11437,"msg":str(e)})

#新增通道(后端做)
@login_required
def add_channel(request):
    try:
        json_str = request.body
        json_obj = json.loads(json_str)
        status = json_obj.get('status')
        rtsp_url = json_obj.get('rtsp_url')
        channel_name = json_obj.get('channel_name')
        if channel.objects.filter(channel_name=channel_name).exists():
            return JsonResponse({'code': 11404, 'msg': '通道名称已经存在'})

        channel.objects.create(
            status=status,
            rtsp_url=rtsp_url,
            channel_name=channel_name,
        )

        return JsonResponse({'code': 200, 'msg': '新增通道成功'})

    except json.JSONDecodeError:
        return JsonResponse({'code': 11405, 'msg': '无效的JSON格式'})


# 新增算法配置(后端做)
@login_required
def add_algorithm(request):
        try:
            json_str = request.body
            json_obj = json.loads(json_str)
            human_alert_type = json_obj.get('human_alert_type')
            car_alert_type = json_obj.get('car_alert_type')
            car_switch_status = json_obj.get('car_switch_status')
            human_switch_status = json_obj.get('human_switch_status')
            human_sensitivity = json_obj.get('human_sensitivity')
            car_sensitivity = json_obj.get('car_sensitivity')
            human_report_frequency = json_obj.get('human_report_frequency')
            car_report_frequency = json_obj.get('car_report_frequency')

            algorithm.objects.create(
                human_alert_type=human_alert_type,
                car_alert_type=car_alert_type,
                car_switch_status=car_switch_status,
                human_switch_status=human_switch_status,
                car_sensitivity=car_sensitivity,
                human_sensitivity=human_sensitivity,
                human_report_frequency=human_report_frequency,
                car_report_frequency=car_report_frequency
            )
            return JsonResponse({'code': 200, 'msg': '新增算法配置成功'})

        except json.JSONDecodeError:
            return JsonResponse({'code': 11410, 'msg': '无效的JSON格式'})


#修改通道信息
@login_required
def update_channel(request):
        try:
            # 获取通道ID
            channel_id = request.GET.get('id')
            if not channel_id:
                return JsonResponse({'code': 11411, 'msg': '通道ID不能为空'})

            # 获取通道对象
            channel_obj = channel.objects.get(id=channel_id )
        except channel.DoesNotExist:
            return JsonResponse({'code': 11412, 'msg': '通道不存在'})
        except Exception as e:
            return JsonResponse({'code': 11413, 'msg': '服务器内部错误'})

        try:
            # 解析JSON数据
            json_str = request.body
            json_obj = json.loads(json_str)
            channel_name = json_obj.get('channel_name')
            rtsp_url = json_obj.get('rtsp_url')

            # 更新通道信息
            if channel_name:
                channel_obj.channel_name = channel_name
            if rtsp_url:
                channel_obj.rtsp_url = rtsp_url
            channel_obj.save()

            return JsonResponse({'code': 200, 'msg': '通道信息修改成功'})

        except json.JSONDecodeError:
            return JsonResponse({'code': 11414, 'msg': '无效的JSON格式'})
        except Exception as e:
            return JsonResponse({'code': 11415, 'msg': '服务器内部错误'})


#修改算法配置
@login_required
def update_algorithm(request):
        try:
            # 获取算法ID
            algorithm_id = request.GET.get('id')
            if not algorithm_id:
                return JsonResponse({'code': 11416, 'msg': '算法ID不能为空'})

            # 获取算法对象
            algorithm_obj = algorithm.objects.get(id=algorithm_id)
        except algorithm.DoesNotExist:
            return JsonResponse({'code': 11417, 'msg': '算法配置不存在'})

        try:
            # 解析JSON数据
            json_str = request.body
            json_obj = json.loads(json_str)
            human_switch_status = json_obj.get('human_switch_status')
            car_switch_status = json_obj.get('car_switch_status')
            human_report_frequency = json_obj.get('human_report_frequency')
            car_report_frequency = json_obj.get('car_report_frequency')
            human_sensitivity = json_obj.get('human_sensitivity')
            car_sensitivity = json_obj.get('car_sensitivity')

            # 更新算法配置
            algorithm_obj.human_switch_status = human_switch_status
            algorithm_obj.car_switch_status = car_switch_status
            algorithm_obj.human_report_frequency = human_report_frequency
            algorithm_obj.car_report_frequency = car_report_frequency
            algorithm_obj.human_sensitivity = human_sensitivity
            algorithm_obj.car_sensitivity = car_sensitivity
            algorithm_obj.save()

            return JsonResponse({'code': 200, 'msg': '算法配置修改成功'})

        except json.JSONDecodeError:
            return JsonResponse({'code': 11419, 'msg': '无效的JSON格式'})
        except Exception as e:
            return JsonResponse({'code': 11420, 'msg': '服务器内部错误'})


#重启通道
@login_required
def reboot_channel(request):
    try:
        # 获取通道ID
        channel_id = request.GET.get('id')
        if not channel_id:
            return JsonResponse({'code': 11421, 'msg': '通道ID不能为空'})

        # 获取通道对象
        channel_obj = channel.objects.get(id=channel_id,)
    except channel.DoesNotExist:
        return JsonResponse({'code': 11422, 'msg': '通道不存在'})
    except Exception as e:
        return JsonResponse({'code': 11423, 'msg': '服务器内部错误'})
    try:
        # 重启通道
        channel_obj.status='离线'
        channel_obj.save()
        channel_obj.status='在线'
        channel_obj.save()

        return JsonResponse({'code': 200, 'msg': '通道重启成功'})

    except json.JSONDecodeError:
        return JsonResponse({'code': 11424, 'msg': '无效的JSON格式'})
    except Exception as e:
        return JsonResponse({'code': 11425, 'msg': '服务器内部错误'})


#重置算法配置
@login_required
def reset_algorithm(request):
    try:
        # 获取配置ID
        algorithm_id = request.GET.get('id')
        if not algorithm_id:
            return JsonResponse({'code': 11426, 'msg': '算法ID不能为空'})

        # 获取算法对象
        algorithm_obj = algorithm.objects.get(id=algorithm_id )
    except algorithm.DoesNotExist:
        return JsonResponse({'code': 11427, 'msg': '算法配置不存在'})
    except Exception as e:
        return JsonResponse({'code': 11428, 'msg': '服务器内部错误'})

    try:
        # 重置算法配置
        algorithm_obj.human_switch_status = "关"
        algorithm_obj.car_switch_status = "关"
        algorithm_obj.human_sensitivity = "60"
        algorithm_obj.car_sensitivity = "60"
        algorithm_obj.human_report_frequency = "5"
        algorithm_obj.car_report_frequency = "5"
        algorithm_obj.save()

        return JsonResponse({'code': 200, 'msg': '算法配置修改成功'})

    except json.JSONDecodeError:
        return JsonResponse({'code': 11429, 'msg': '无效的JSON格式'})
    except Exception as e:
        return JsonResponse({'code': 11430, 'msg': '服务器内部错误'})


#重置配置到所有
@login_required
def reset_all_algorithm(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    human_switch_status = json_obj.get('human_switch_status')
    car_switch_status = json_obj.get('car_switch_status')
    human_sensitivity = json_obj.get('human_sensitivity')
    car_sensitivity = json_obj.get('car_sensitivity')
    human_report_frequency = json_obj.get('human_report_frequency')
    car_report_frequency = json_obj.get('car_report_frequency')

    try:
        # 获取所有算法配置
        algorithms = algorithm.objects.all()

        # 定义默认配置
        default_config = {
            'human_switch_status': human_switch_status,
            'car_switch_status': car_switch_status,
            'human_sensitivity': human_sensitivity,
            'car_sensitivity': car_sensitivity,
            'human_report_frequency': human_report_frequency,
            'car_report_frequency': car_report_frequency,
        }

        # 批量更新所有算法配置
        algorithms.update(**default_config)

        return JsonResponse({'code': 200, 'msg': '算法配置修改成功'})

    except Exception as e:
        return JsonResponse({'code': 11431, 'msg': '服务器内部错误'})


# 删除通道数据(后端)
@login_required
def delete_channel(request):
    try:
        channel_id = request.GET.get('id')
        if not channel_id:
            return JsonResponse({'code': 11432, 'msg': '通道数据不能为空'})
        # 获取通道对象
        channel_obj = channel.objects.get(id=channel_id )
    except channel.DoesNotExist:
        return JsonResponse({'code': 11433, 'msg': '通道数据不存在'})

    # 删除数据库记录
    channel_obj.is_active = False
    channel_obj.save()

    return JsonResponse({'code': 200, 'msg': '通道删除成功'})


#删除算法配置(后端)
@login_required
def delete_algorithm(request):
    try:
        algorithm_id = request.GET.get('id')
        if not algorithm_id:
            return JsonResponse({'code': 11434, 'msg': '算法配置不能为空'})
        # 获取通道对象
        algorithm_obj = algorithm.objects.get(id=algorithm_id )
    except algorithm.DoesNotExist:
        return JsonResponse({'code': 11435, 'msg': '算法配置不存在'})

    # 删除数据库记录
    algorithm_obj.is_active = False
    algorithm_obj.save()

    return JsonResponse({'code': 200, 'msg': '算法配置删除成功'})