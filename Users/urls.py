from django.urls import path

from Users import views
from Users.views import Loginview, Logoutview, Registerview

urlpatterns = [
    path('login',Loginview.as_view(),name='用户登录'),
    path('logout',Logoutview.as_view(),name='用户退出'),
    path('register',Registerview.as_view(),name='用户注册'),
]