#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 用户相关

from wx.tabels import User as t_user
from wx.tabels import Activity as t_activity
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
# from wx.sqlConnect import session
from wx import sqlConnect
from wx.sqlCommon import returnFormat, generate_token, getUserToken, validToken, getUserByToken
db = sqlConnect.DbMgr()
session = db.session

# 获取用户信息
def getUser (arg):
  openId = arg['openId']
  tokenGet = arg['token']
  results = session.query(t_user).filter(t_user.openId==openId).all()
  session.close()
  if len(results) == 0 :
    results = False
  else:
    results = results[0]

  if not results :
    return returnFormat('', '用户不存在', '901')
  obj = {}
  id = results.id
  name = results.name
  token = results.token
  obj['userId'] = id
  obj['nickName'] = name
  obj['openId'] = results.openId
  valid = False
  if tokenGet == token :
    valid = validToken(token)
  else:
    return returnFormat('', 'token无效', '701')
  if valid == False :
    return returnFormat('', 'token过期', '701')

  return returnFormat(obj)

# 根据id获取用户信息
def getUserById (arg, userInfo):
  print('用户信心token', userInfo)
  userId = arg['userId']
  # sql2 = 'select * from user where id="%s"' % (userId)
  results = session.query(t_user).filter(t_user.id==userId).all()
  print('用户信息', results)
  if userInfo == '1' or userInfo == '2':
    return returnFormat('', 'token无效', '701')

  if len(results) == 0 :
    results = False
  else:
    arry = []
    dic = {
      'id': fields.String,
      'name': fields.String,
      'openId': fields.String,
      'token': fields.String,
      'phone': fields.String,
      'city': fields.String,
      'auth': fields.String,
      'avatarUrl': fields.String,
      'age': fields.String
    }
    for item in results:
      print('用户信息', item.id)
      arry.append(item)
    results =  marshal(arry, dic)
    results = results[0]
    print('用户信息', results)
  session.close()
  if not results :
    return returnFormat('', '用户不存在', '901')
  return returnFormat(results)

# 获取游戏认证状态
def gameStatus (arg, userInfo):
  userId = userInfo['id']
