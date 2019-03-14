"""max URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from wx import views as max_views
urlpatterns = [
    path('server/app/user/detail', max_views.getUser, name="getUser"), # 获取用户信息详情
    path('api/login', max_views.login, name="login"),
    path('server/app/reg/register', max_views.register, name="register"), # 注册
    path('api/activityList', max_views.activityList, name="activityList"),
    path('api/upload/token', max_views.uploadToken, name="uploadToken"),
    path('api/upload/void/token', max_views.uploadToken, name="voidToken"),
    path('api/add/activity', max_views.addActivity, name="addActivity"),
    path('api/auth', max_views.auth, name="auth"),
    path('api/userinfo/id', max_views.getUserById, name="getUserById"),
    path('api/getMsg', max_views.getMsg, name="getMsg"),
    path('api/read/msg', max_views.readMsg, name="readMsg"),
    path('api/unread/msg', max_views.getUnReadMsg, name="getUnReadMsg"),
    path('api/add/msg', max_views.addMsg, name="addMsg"),
    path('api/join/activity', max_views.joinActivity, name="joinActivity"),
    path('index', max_views.index, name="index"),
    path('index1', max_views.index1, name="index1"),
    path('admin/', admin.site.urls)
]
