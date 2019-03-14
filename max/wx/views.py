# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from wx import models, upload, loginReg, sqlUser, sqlActivity, sqlAuth
from wx import socket1
from wx.sqlCommon import getUserByToken, returnFormat
# from wx import upload
import json
socket1.on()
def action (request, sqlFn, isValidAuth=1):
  print('签名')
  print(request.META.get("HTTP_AUTH"))
  if request.method == 'GET' :
    params = request.GET.dict()
  else:
    params = json.loads(request.body)

  if isValidAuth == 1:
      auth = request.META.get("HTTP_AUTH")
      sqlReuslt = getUserByToken(auth)
      if sqlReuslt == 1 or sqlReuslt == 3:
        sqlReuslt = returnFormat('', 'token无效', '701')
      else:
        sqlReuslt = sqlFn(params, sqlReuslt)
  else:
    sqlReuslt = sqlFn(params)

  return HttpResponse(json.dumps(sqlReuslt, ensure_ascii=False), content_type='application/json; charset=utf-8')
  # return HttpResponse(sqlReuslt, content_type='application/json; charset=utf-8')

def getUser(request):
  return action(request, sqlUser.getUser)

def login(request):
  return action(request, loginReg.login, 0)

def register(request):
  return action(request, loginReg.register, 0)

def activityList(request):
  return action(request, sqlActivity.activityList)

def joinActivity(request):
  return action(request, sqlActivity.joinActivity)

def uploadToken(request):
  return action(request, upload.upload)

def addActivity(request):
  return action(request, sqlActivity.addActivity)

def uploadVoidToken(request):
  return action(request, upload.uploadVoid)

def auth(request):
  return action(request, sqlAuth.auth)

def getUserById(request):
  return action(request, sqlUser.getUserById)

def index(request):
    return render(request, 'index3.html')

def index1(request):
    return render(request, 'index1.html')

def getMsg(request):
  return action(request, models.getMsg)

def readMsg(request):
  return action(request, models.readChatMsg)

def getUnReadMsg(request):
  return action(request, models.getUnReadMsgByUser)

def addMsg(request):
  return action(request, models.addMsg)
