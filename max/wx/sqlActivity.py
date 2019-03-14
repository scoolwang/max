#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 活动相关

from wx.tabels import User as t_user
from wx.tabels import Activity as t_activity
from wx.tabels import Game as t_game
from wx.tabels import Passenger as t_passenger
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

# 查询所有活动
def activityList (arg, userInfo):
  page = int(arg['page']) - 1
  pageSize = int(arg['pageSize'])

  results = session.query(t_activity, t_user.name, t_game.name, t_game.logo).join(t_user, t_activity.userId == t_user.id).join(t_game, t_activity.gameId==t_game.id).limit(pageSize).offset(page * pageSize)
  # results = session.query(t_activity, t_user.name, t_game.name, t_game.logo).join(t_user, t_activity.userId == t_user.id).join(t_game, t_activity.gameId==t_game.id).all()
  session.close()
  arry = []
  for item, usernName, gameName, gameLogo in results :
    item.userNName = usernName
    item.gameName = gameName
    item.gameLogo = gameLogo
    arry.append(item)

  dic = {
    'id': fields.String, # 活动ID
    'gameId': fields.String, # 游戏ID
    'gameName': fields.String, # 游戏名字
    'gameLogo': fields.String, # 游戏图标
    'userName': fields.String, # 用户名
    'userId': fields.String, # 用户id
    'cover': fields.String, # 活动封面
    'desc': fields.String(attribute='detail'), # 描述
    'startTime': fields.String, # 发车时间
    'createTime': fields.String, # 发帖时间
    'vacancy': fields.String, # 空位
    'seat': fields.String, # 座位总数
  }
  results =  marshal(arry, dic)
  print('活动', results)
  if len(results) == 0 :
    results = []
  else:
    results = results
  return returnFormat(results)

# 发布活动
def addActivity (arg, userInfo):
  # startTime = int(arg['startTime'])
  startTime = int(arg['startTime'])
  desc = arg['desc']
  seat = int(arg['seat'])
  # city = arg['city']
  cover = arg['cover']
  gameId = arg['gameId']
  activityId = str(uuid.uuid1())
  createTime = int(round(time.time() * 1000))
  if startTime == '':
    startTime = 0
  else:
    startTime = int(startTime)

  userId = userInfo.id
  results = t_activity(id=activityId, gameId=gameId, cover=cover, detail=desc, startTime=startTime, createTime=createTime, seat=seat, userId=userId, vacancy=0)
  session.add(results)
  session.commit()
  session.close()
  # sql = 'insert into activity (id, userId, createTime, startTime, t_desc, t_limit, t_left, cover, gameId) values ("%s", "%s", "%d", "%d", "%s", "%d", "%d", "%s", "%s")' % (activityId, userId, createTime, startTime, desc, limit, 0, cover, gameId)
  print(results)
  # results = runSql(sql)
  return returnFormat('', '发布成功')

# 参加活动
def joinActivity (arg, userInfo):
  id = str(uuid.uuid1())
  activityId = arg['id']
  detail = arg['detail']
  createTime = int(time.time() * 1000)
  print('时间', createTime)
  userId = userInfo.id
  status = 1
  results = session.query(t_passenger).filter(t_passenger.userId==userId).all()
  if len(results) > 0:
    return returnFormat('', '已申请过', '901')

  row = t_passenger(id=id, activityId=activityId, detail=detail, createTime=createTime, userId=userId, status=status)
  session.add(row)
  session.commit()
  session.close()
  return returnFormat('', '参加成功')

# # 认证
# def auth (arg):
#   token = arg['token']
#   gameId = int(arg['gameId'])
#   voidSrc = arg['voidSrc']
#   gameImg = arg['gameImg']
#   sex = arg['sex']
#   age = arg['age']
#   authId = str(uuid.uuid1())
#   userInfo = getUserByToken(token)
#   print(userInfo)
#   if userInfo == '1' or userInfo == '2':
#     return returnFormat('', 'token无效', '701')
#   else:
#     userId = userInfo['id']
#     sql = 'insert into auth (id, userId, gameId, voidSrc, gameImg, sex, age) values ("%s", "%s", "%d", "%s", "%s", "%s", "%s")' % (authId, userId, gameId, voidSrc, gameImg, sex, age)
#     print(sql)
#     results = runSql(sql)
#     return returnFormat('', '提交成功')

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









