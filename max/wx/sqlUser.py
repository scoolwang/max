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
from wx.sqlConnect import session
from wx.sqlCommon import returnFormat, generate_token, getUserToken, validToken, getUserByToken


# 获取用户信息
def getUser (arg):
  openId = arg['openId']
  tokenGet = arg['token']
  results = session.query(t_user).filter(t_user.openId==openId).all()
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
  tokenGet = arg['token']
  userId = arg['userId']
  userInfo = getUserByToken(tokenGet)
  # sql2 = 'select * from user where id="%s"' % (userId)
  results = session.query(t_user).filter(t_user.id==userId).all()
  session.close()
  if userInfo == '1' or userInfo == '2':
    return returnFormat('', 'token无效', '701')

  if len(results2) == 0 :
    results2 = False
  else:
    results2 = results2[0]

  if not results2 :
    return returnFormat('', '用户不存在', '901')
  return returnFormat(results2)










