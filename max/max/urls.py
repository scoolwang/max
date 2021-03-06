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
    path('api/get/user', max_views.getUser, name="getUser"), # 获取用户信息详情
    path('api/login', max_views.login, name="login"),
    path('api/register', max_views.register, name="register"), # 注册
    path('api/activityList', max_views.activityList, name="activityList"),
    path('api/upload/token', max_views.uploadToken, name="uploadToken"),
    path('api/upload/void/token', max_views.uploadToken, name="voidToken"),
    path('api/add/activity', max_views.addActivity, name="addActivity"),
    path('api/auth', max_views.auth, name="auth"),
    path('api/userinfo/id', max_views.getUserById, name="getUserById"),
    path('api/getMsg', max_views.getMsg, name="getMsg"),
    path('api/read/msg', max_views.readMsg, name="readMsg"),
    path('api/unread/msg', max_views.getUnReadMsg, name="getUnReadMsg"),
    path('api/sys/msg', max_views.getSysMsg, name="getSysMsg"),
    path('api/unread/chat/msg', max_views.getChatUnreadMsg, name="getChatUnreadMsg"),
    path('api/add/msg', max_views.addMsg, name="addMsg"),
    path('api/join/activity', max_views.joinActivity, name="joinActivity"),
    path('api/get/activity', max_views.activityDetail, name="activityDetail"),
    path('api/get/activity/users', max_views.getActivityUsers, name="getActivityUsers"),
    path('api/get/activity/status', max_views.editStatus, name="editStatus"),
    path('api/add/comment', max_views.addComment, name="addComment"),
    path('api/get/comment', max_views.getComment, name="getComment"),
    path('api/get/load', max_views.load, name="load"),
    path('index', max_views.index, name="index"),
    path('index1', max_views.index1, name="index1"),
    path('admin/', admin.site.urls),
    path('api/get/reply', max_views.getReply, name="getReply"),
    path('api/get/auth', max_views.gameStatus, name="gameStatus"),
    path('api/user/update', max_views.updateUser, name="updateUser"),
    path('api/user/auth', max_views.userAuth, name="userAuth"),
    path('api/get/join', max_views.getMyJoin, name="getMyJoin"),
    path('api/recall/join', max_views.recallJoin, name="recallJoin"),
    path('api/game/info', max_views.getGameInfo, name="getGameInfo"),
    path('api/care/user', max_views.careUser, name="careUser"),
    path('api/user/auth/game', max_views.userAuthGame, name="userAuthGame"),
    path('api/add/words', max_views.commentUser, name="commentUser"),
    path('api/get/words', max_views.getWords, name="getWords"),
    path('api/get/gamelist', max_views.getGameList, name="getGameList"),
    path('api/get/fans', max_views.getFansList, name="getFansList"),
    path('api/get/care', max_views.getCareList, name="getCareList"),
    path('api/unread/msg/total', max_views.getUnreadMsgTotal, name="getUnreadMsgTotal"),
    path('api/read/msg/id', max_views.readMsgById, name="readMsgById")

]
