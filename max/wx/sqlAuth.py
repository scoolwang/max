#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 认证相关

from wx.tabels import User as t_user
from wx.tabels import Activity as t_activity
from wx.tabels import Game as t_game
from wx.tabels import Auth as t_auth

# from wx import tabels as
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from django.core import serializers
from flask_restful import reqparse, fields, marshal, marshal_with
import json
import time
import base64
import hmac
import uuid
from wx.sqlConnect import session
from wx.sqlCommon import returnFormat, generate_token, getUserToken, validToken, getUserByToken

def sql_result_to_json(result):
  if type(result) is dict:
      return result.to_dict()
  else:
      arr = []
      for item in result:
        obj = {}
        for k, v in item.__dict__.items():
            if k != '_sa_instance_state':
              obj[k] = v

        arr.append(obj)
      return arr

# 认证
def auth (arg, userInfo):
  gameId = int(arg['gameId'])
  voidSrc = arg['voidSrc']
  gameImg = arg['gameImg']
  detail = arg['desc']
  levelId = int(arg['levelId'])
  sex = int(arg['sex'])
  authId = str(uuid.uuid1())
  print('用户信息', userInfo)
  userId = userInfo.id
  # sql = 'insert into auth (id, userId, gameId, voidSrc, gameImg, sex, age) values ("%s", "%s", "%d", "%s", "%s", "%s", "%s")' % (authId, userId, gameId, voidSrc, gameImg, sex, age)
  # print(sql)
  # results = runSql(sql)
  row = t_auth(id=authId, gameId=gameId, voidSrc=voidSrc, detail=detail, gameImg=gameImg, sex=sex, status=0, levelId=levelId, userId=userId)
  session.add(row)
  session.commit()
  session.close()
  return returnFormat('', '提交成功')

# # 添加未读消息
# def addMsg (arg):
#   msgId = str(uuid.uuid1())
#   sendId = arg['sendId']
#   receiveId = arg['receiveId']
#   msg = arg['msg']
#   timeStr = arg['time']
#   msgType = int(arg['type'])
#   status = 0
#   print(arg)
#   print('时间')
#   print(timeStr)
#   # userInfo = getUserByToken(token)
#   # if userInfo == '1' or userInfo == '2':
#   #   return returnFormat('', 'token无效', '701')
#   # else:
#   sql = 'insert into message (id, sendId, receiveId, msg, time, type, status) values ("%s", "%s", "%s", "%s", "%d", "%d", "%d")' % (msgId, sendId, receiveId, msg, timeStr, msgType, status)
#   print(sql)
#   results = runSql(sql)
#   return returnFormat('', '添加成功')

# # 获取未读消息列表
# def getMsg (arg):
#   token = arg['token']
#   userInfo = getUserByToken(token)
#   print('用户信心')
#   print(userInfo)
#   print('用户信心1')
#   if userInfo == '1' or userInfo == '2':
#     return returnFormat('', 'token无效', '701')
#   else:
#     userId = userInfo['id']
#     print('信息查询')
#     sql = 'select t1.*, t2.name, t2.avatarUrl from message as t1, user as t2 where t1.receiveId= "%s" and t1.status=0 and t2.id=t1.sendId order by t1.time ASC' % (userId)
#     print(sql)
#     results = runSql(sql)
#     return returnFormat(results, 'success')

# #标记消息为已读状态
# def readChatMsg (arg):
#   sendId = arg['id']
#   token = arg['token']
#   userInfo = getUserByToken(token)
#   print('用户信心')
#   print(userInfo)
#   print('用户信心1')
#   if userInfo == '1' or userInfo == '2':
#     return returnFormat('', 'token无效', '701')
#   else:
#     userId = userInfo['id']
#     sql = 'update message set status=1 where receiveId="%s" and sendId="%s"' % (userId, sendId)
#     results = runSql(sql)
#     return returnFormat('', '')

# # 获取用户的未读消息
# def getUnReadMsgByUser (arg):
#   print('获取用户的未读消息')
#   print(arg)
#   sendId = arg['id']
#   token = arg['token']
#   userInfo = getUserByToken(token)
#   if userInfo == '1' or userInfo == '2':
#     return returnFormat('', 'token无效', '701')
#   else:
#     userId = userInfo['id']
#     sql = 'select * from message where receiveId="%s" and sendId="%s" and status=0' % (userId, sendId)
#     results = runSql(sql)
#     readChatMsg({
#       'id': sendId,
#       'token': token
#     })
#     return returnFormat(results, '拉取用户未读消息')









