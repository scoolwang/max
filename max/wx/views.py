# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from wx import models, upload, loginReg, sqlUser, sqlActivity, sqlAuth, sqlMsg
from wx import socket1
from wx.sqlCommon import getUserByToken, returnFormat
from wx.sqlConnect import session
# from wx import upload
import json
socket1.on()
def action (request, sqlFn, isValidAuth=1):
  # print('签名', request.META.get("HTTP_ACCESS_TOKEN"))
  # print('签名2', request.META.get("HTTP_CLIENT"))
  # print(request.META.get("HTTP_ACCESS_TOKEN"))
  if request.method == 'GET' :
    params = request.GET.dict()
  else:
    params = json.loads(request.body)

  # print('签名2', params)
  if isValidAuth == 1:
      auth = request.META.get("HTTP_ACCESS_TOKEN")
      print('获取token', auth)
      print('获取params', params)
      sqlReuslt = getUserByToken(auth, params['openId'])
      if sqlReuslt == '1' or sqlReuslt == '2':
        sqlReuslt = returnFormat('', 'token无效', '701')
      else:
        # print(sqlReuslt['id'], '用户id')
        # try:
        sqlReuslt = sqlFn(params, sqlReuslt)
        # except Exception as e:
        # print('mysql异常', e)
        # session.rollback()

  else:
    sqlReuslt = sqlFn(params)

  # print('***********返回数据start***************')
  # print(json.dumps(sqlReuslt, ensure_ascii=False))
  # print('***********返回数据end***************')
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
  return action(request, upload.upload, 0)

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
  return action(request, sqlMsg.getMsg)

def readMsg(request):
  return action(request, sqlMsg.readChatMsg)

def getUnReadMsg(request):
  return action(request, sqlMsg.getUnReadMsgByUser)

def addMsg(request):
  return action(request, models.addMsg)

def getSysMsg(request):
  return action(request, sqlMsg.getSysMsg)

def getChatUnreadMsg(request):
  return action(request, sqlMsg.getChatUnreadMsg)

def activityDetail(request):
  return action(request, sqlActivity.activityDetail)

def getActivityUsers(request):
  return action(request, sqlActivity.getActivityUsers)

def editStatus(request):
  return action(request, sqlActivity.editStatus)

def addComment(request):
  return action(request, sqlActivity.addComment)

def getComment(request):
  return action(request, sqlActivity.getComment)

def load(request):
  return action(request, upload.load, 0)

def getReply(request):
  return action(request, sqlActivity.getReply)

def gameStatus(request):
  return action(request, sqlUser.gameStatus)

def updateUser(request):
  return action(request, sqlUser.updateUser)

def userAuth(request):
  return action(request, sqlUser.userAuth)

def getMyJoin(request):
  return action(request, sqlActivity.getMyJoin)

def recallJoin(request):
  return action(request, sqlActivity.recallJoin)

def getGameInfo(request):
  return action(request, sqlAuth.getGameInfo)

def careUser(request):
  return action(request, sqlUser.careUser)

def userAuthGame(request):
  return action(request, sqlUser.userAuthGame)

def commentUser(request):
  return action(request, sqlActivity.commentUser)

def getWords(request):
  return action(request, sqlUser.getWords)

def getGameList(request):
  return action(request, sqlAuth.getGameList, 0)

def getFansList(request):
  return action(request, sqlUser.getFansList)

def getCareList(request):
  return action(request, sqlUser.getCareList)

def getUnreadMsgTotal(request):
  return action(request, sqlMsg.getUnreadMsgTotal)
def readMsgById(request):
  return action(request, sqlMsg.readMsgById)


