# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from wx import models, upload
# from wx import upload
import json

def action (request, sqlFn):
  if request.method == 'GET' :
    params = request.GET.dict()
  else:
    params = json.loads(request.body)
  sqlReuslt = sqlFn(params)
  print(params)
  return HttpResponse(json.dumps(sqlReuslt, ensure_ascii=False), content_type='application/json; charset=utf-8')

def getUser(request):
  return action(request, models.getUser)

def login(request):
  return action(request, models.login)

def register(request):
  return action(request, models.register)

def activityList(request):
  return action(request, models.activityList)

def uploadToken(request):
  print(upload)
  return action(request, upload.upload)

def addActivity(request):
  return action(request, models.addActivity)

