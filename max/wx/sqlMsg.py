#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from wx.tabels import Message as t_message
from wx.tabels import Activity as t_activity
from wx.tabels import User as t_user
# from wx import tabels as
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from django.core import serializers
from flask_restful import reqparse, fields, marshal
import json
import time
import base64
import hmac
import uuid
import datetime
import arrow
# from wx.sqlConnect import session
from wx import sqlConnect
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from wx.aescrypt import EncryptAES
from wx.sqlCommon import returnFormat, generate_token, getUserToken, validToken, getUserByToken
aes = EncryptAES()
db = sqlConnect.DbMgr()
session = db.session
# 添加未读消息
def addMsg (arg):
  msgId = str(uuid.uuid1())
  sendId = arg['sendId']
  receiveId = arg['receiveId']
  timeStr = arg['time']
  startTime = int(timeStr)
  startTime = datetime.datetime.fromtimestamp(startTime/1000)
  msgType = int(arg['type'])
  status = 0
  msgStr = json.dumps(arg['data'], ensure_ascii=False)
  # print(arg)
  # print('时间')
  # userInfo = getUserByToken(token)
  # if userInfo == '1' or userInfo == '2':
  #   return returnFormat('', 'token无效', '701')
  # else:
  # sql = 'insert into message (id, sendId, receiveId, msg, time, type, status) values ("%s", "%s", "%s", "%s", "%d", "%d", "%d")' % (msgId, sendId, receiveId, msg, timeStr, msgType, status)
  row = t_message(id=msgId, sendId=sendId, receiveId=receiveId, msg=msgStr, time=startTime, msgType=msgType, status=0)
  session.add(row)
  session.commit()
  session.close()
  return returnFormat('', '添加成功')


# # 获取用户的未读消息并修改消息状态
def getUnReadMsgByUser (arg, userInfo):
  # print('获取用户的未读消息')
  # print(userInfo)
  sendId = arg['id']

  userId = userInfo['id']
  results = session.query(t_message).filter(t_message.receiveId==userId, t_message.msgType==1, t_message.status==0).all()
  for item in results:
    item.timeNum = arrow.get(item.time).timestamp * 1000
    print(item.status, '结果集')

  # sql = 'select * from message where receiveId="%s" and sendId="%s" and status=0' % (userId, sendId)
  # results = runSql(sql)
  # arry = []
  # print(results)

    # arry.append(item)

  dic = {
    'id': fields.String,
    'sendId': fields.String,
    'receiveId': fields.String,
    'type': fields.String(attribute='msgType'),
    'time': fields.Integer(attribute='timeNum'),
    'data': fields.String(attribute='msg')
  }
  results =  marshal(results, dic)
  print('用户消息', results)
  session.close()
  readChatMsg({
    'receiveId': userId,
    'sendId': sendId
  })
  return returnFormat(results, '拉取用户未读消息')

# # 获取用户的未读消息不修改消息状态
def getChatUnreadMsg ():
  # print('获取用户的未读消息')
  # print(userInfo)

  userId = userInfo['id']
  results = session.query(t_message).filter(t_message.receiveId==userId, t_message.msgType==1, t_message.status==0).all()
  for item in results:
    item.timeNum = arrow.get(item.time).timestamp * 1000
    print(item.status, '结果集')

  # sql = 'select * from message where receiveId="%s" and sendId="%s" and status=0' % (userId, sendId)
  # results = runSql(sql)
  # arry = []
  # print(results)

    # arry.append(item)

  dic = {
    'id': fields.String,
    'sendId': fields.String,
    'receiveId': fields.String,
    'type': fields.String(attribute='msgType'),
    'time': fields.Integer(attribute='timeNum'),
    'data': fields.String(attribute='msg')
  }
  results =  marshal(results, dic)
  print('用户消息', results)
  session.close()
  return returnFormat(results, '拉取用户未读消息不修改状态')

# 获取系统消息
def getSysMsg (arg, userInfo):
  # print('获取用户的未读消息')
  # print(userInfo)
  unReadNum = 0
  userId = userInfo['id']
  results = session.query(t_message, t_user.avatarUrl).join(t_user, t_message.sendId == t_user.id).filter(t_message.receiveId==userId, t_message.msgType==2).all()
  for item, avatarUrl in results:
    item.sendAvatarUrl =  avatarUrl
    item.timeNum = arrow.get(item.time).timestamp * 1000
    if item.status == 0:
      unReadNum += 1
    print(item.status, '结果集')

  # sql = 'select * from message where receiveId="%s" and sendId="%s" and status=0' % (userId, sendId)
  # results = runSql(sql)
  # arry = []
  # print(results)

    # arry.append(item)

  dic = {
    'id': fields.String,
    'sendAvatarUrl': fields.String,
    'sendId': fields.String,
    'receiveId': fields.String,
    'type': fields.String(attribute='msgType'),
    'time': fields.Integer(attribute='timeNum'),
    'data': fields.String(attribute='msg')
  }
  results =  marshal(results, dic)
  print('用户消息', results)
  session.close()
  return returnFormat({'list': results, 'unReadNum': unReadNum}, '拉取系统未读消息')

# 获取上车消息
def getApplyMsg (arg, userInfo):
  unReadNum = 0
  userId = userInfo['id']
  results = session.query(t_message).filter(t_message.receiveId==userId, t_message.msgType==3).all()
  for item in results:
    item.timeNum = arrow.get(item.time).timestamp * 1000
    if item.status == 0:
      unReadNum += 1
    print(item.status, '结果集')

  # sql = 'select * from message where receiveId="%s" and sendId="%s" and status=0' % (userId, sendId)
  # results = runSql(sql)
  # arry = []
  # print(results)

    # arry.append(item)

  dic = {
    'id': fields.String,
    'sendId': fields.String,
    'receiveId': fields.String,
    'type': fields.String(attribute='msgType'),
    'time': fields.Integer(attribute='timeNum'),
    'data': fields.Nested(attribute='msg')
  }
  results =  marshal(results, dic)
  print('用户消息', results)
  session.close()
  readChatMsg({
    'receiveId': userId,
    'sendId': '001'
  })
  return returnFormat({'list': results, 'unReadNum': unReadNum}, '拉取上车未读消息')

def getMsg(arg, userInfo):
  userId = userInfo['id']
  # results1 = session.query(t_message, t_user.avatarUrl).join(t_user, t_message.sendId == t_user.id).filter(t_message.receiveId==userId, t_message.msgType==1, t_message.status==0).all()
  results1 = session.query(t_message, t_user.avatarUrl, t_user.name).join(t_user, t_message.sendId == t_user.id).filter(t_message.receiveId==userId, t_message.msgType==1, t_message.status==0).all()
  # json.dumps(sqlReuslt, ensure_ascii=False)
  session.close()

  results2 = session.query(t_message, t_user.avatarUrl, t_user.name).join(t_user, t_message.sendId == t_user.id).filter(t_message.receiveId==userId, t_message.msgType==2).all()
  session.close()

  results3 = session.query(t_message, t_user.avatarUrl, t_user.name).join(t_user, t_message.sendId == t_user.id).filter(t_message.receiveId==userId, t_message.msgType==3).all()
  session.close()

  arry1 = []
  arry2 = []
  arry3 = []
  for item, avatarUrl, name in results1 + results2 + results3:
    item.data = json.loads(item.msg)
    item.data['sendAvatar'] = avatarUrl
    item.data['sendName'] = name

    item.timeNum = arrow.get(item.time).timestamp * 1000
    if item.msgType==1:
      arry1.append(item)
    if item.msgType==2:
      arry2.append(item)
    if item.msgType==3:
      arry3.append(item)
  dic = {
    'id': fields.String,
    'status': fields.Integer,
    'sendId': fields.String,
    'receiveId': fields.String,
    'type': fields.String(attribute='msgType'),
    'time': fields.Integer(attribute='timeNum'),
    'data': fields.Raw
  }
  dic2 = {
    'avatarUrl': fields.String
  }
  print(len(results1), '集合长度')
  results1 =  marshal(arry1, dic)
  results2 =  marshal(arry2, dic)
  results3 =  marshal(arry3, dic)
  session.close()
  print(results1, '集合长度')
  print(len(results1), '集合长度')
  return returnFormat({'chat': results1, 'sys': results2, 'apply': results3}, '消息页面')
  # return returnFormat(results1, '消息页面')

#标记消息为已读状态
def readChatMsg (arg):
  receiveId = arg['receiveId']
  sendId = arg['sendId']
  print('更新成功2')
  results = session.query(t_message).filter(t_message.receiveId==receiveId and t_message.sendId==sendId and status==0).update({t_message.status: 1})
  session.commit()
  session.close()
  print('更新成功')
  return returnFormat('成功', '')

