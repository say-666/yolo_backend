import hashlib
import json
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from Users.models import User

# Create your views here.
def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            session_key = request.COOKIES.get('sessionid')
            try:
                session_id = Session.objects.get(session_key=session_key)
            except ObjectDoesNotExist:
                # 如果 session 不存在，返回未登录的响应
                result = {'code': 11401, 'msg': '未登录'}
                return JsonResponse(result)

            # 如果 session 存在，调用原始视图函数
            return view_func(request, *args, **kwargs)
        except Exception as e:
            # 捕获任何其他异常，并返回错误信息
            print(f"Error in login_required decorator: {e}")
            result = {'code': 11401, 'msg': '未登录或发生错误'}
            return JsonResponse(result)
    # 返回包装完成之后，即通过所有判断之后的函数
    return _wrapped_view

class Registerview(View):
    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        account = json_obj.get('account')
        password_1 = json_obj.get('password_1')
        password_2 = json_obj.get('password_2')

        if account == "":
            result = {'code': 11402, 'msg': '请输入账号'}
            return JsonResponse(result)
        if password_1 == "":
            result = {'code': 11403, 'msg': '请输入密码'}
            return JsonResponse(result)
        if password_2 == "":
            result = {'code': 11404, 'msg': '请再次输入密码'}
            return JsonResponse(result)

        # 两个密码要保持一致，判断并作出响应
        if password_1 != password_2:
            result = {'code': 11405, 'msg': '两次密码输入不一致'}
            return JsonResponse(result)

        #检查用户名是否可用
        old_users = User.objects.filter(account=account)
        if old_users:
            result = {'code': 11407, 'msg': '账号已经存在'}
            return JsonResponse(result)

        #Users插入数据（密码md5存储）
        m = hashlib.md5()
        password_1 = str(password_1)
        m.update(password_1.encode())

        User.objects.create(account=account,password= m.hexdigest())

        result = {'code': 200, 'msg':'注册成功'}
        return JsonResponse(result)

class Loginview(View):
    def post(self, request):

        json_str = request.body
        json_obj = json.loads(json_str)
        account = json_obj.get('account')
        password = json_obj.get('password')

        try:
            user = User.objects.get(Q(account=account))
        except User.DoesNotExist:
            result = {'code': 11408, 'msg': '账号或密码错误'}
            return JsonResponse(result)

        m = hashlib.md5()
        m.update(password.encode())

        user = User.objects.get(account=account)

        if m.hexdigest() != user.password:
            result = {'code': 11409,'msg': '账号或密码错误'}
            return JsonResponse(result)

        request.session['sessionid'] = account
        request.session.save()
        result = {'code': 200,'msg': '登录成功','account':user.account}
        return JsonResponse(result)


class Logoutview(View):
    def post(self, request):
        session_key = request.COOKIES.get('sessionid')
        if session_key:
            session_id = Session.objects.get(session_key=session_key)
            session_id.delete()
            response = JsonResponse({'code': 200, 'msg': '退出成功'})
            response.delete_cookie('sessionid')
            return response
        else:
            return JsonResponse({'code': 114010, 'msg': '未知错误'})