from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from user.models import User
import  hashlib
import json
from django.views import View
from django.contrib.auth import authenticate, login

# Create your views here.
def u_login(request):
    if request.method == 'GET':
        result={'code':200,'need':'跳转登录页面'}
        return JsonResponse(result)
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        username=json_obj['username']
        password=json_obj['password']
        try:
            user=User.objects.get(username=username)
        except Exception as e:
            result={'code':10201,'error':'用户名不存在'}
            return JsonResponse(result)
        p_m=hashlib.md5()
        p_m.update(password.encode('utf-8'))
        if p_m.hexdigest() != user.password:
            result={'code':10202,'error':'用户名或密码不正确'}
            return JsonResponse(result)
        if p_m.hexdigest() == user.password:
            request.session['username']=username
            request.session['password']=password
            request.COOKIES['username']=username
            request.COOKIES['password']=password
            request.session.set_expiry(24*60*60)
            result={'code':200,'msg':'登录成功进入页面'}
            return JsonResponse(result)


def register(request):
    if request.method != 'POST':
        result={"code":10102,"error":"请用post"}
        return JsonResponse(result)
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    password_1 = json_obj['password_1']
    password_2 = json_obj['password_2']
    if password_1 != password_2:
        result = {'code': 10100, 'error': '密码不一致'}
        return JsonResponse(result)
    old_user = User.objects.filter(username=username)
    if old_user:
        result = {'code': 10101, 'error': '用户名已存在'}
        return JsonResponse(result)
    p_m = hashlib.md5()
    p_m.update(password_1.encode('utf-8'))
    User.objects.create(username=username, password=p_m.hexdigest())
    result = {'code': 200,'msg':'注册成功'}
    return JsonResponse(result)

def logout(request):
    if request.method == 'POST':
        if 'username' in request.session:
            del request.session['username']
        if 'password' in request.session:
            del request.session['password']
        resp = HttpResponseRedirect('/api/login')
        if 'username' in request.COOKIES:
            resp.delete_cookie('username')
        if 'password' in request.COOKIES:
            resp.delete_cookie('password')
        result = {'code': 200,'msg':'已经退出登录，返回登录界面'}
        return JsonResponse(result)

def check_login(n):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session or 'password' not in request.session:
            username = request.COOKIES.get('username')
            password= request.COOKIES.get('password')
            if not username or not password:
                return HttpResponseRedirect('/api/login')
            else:
                request.session['username'] = username
                request.session['password'] = password
        return n(request, *args, **kwargs)
    return wrap