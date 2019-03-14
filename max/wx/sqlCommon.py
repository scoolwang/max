#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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



def returnFormat (data, message='', code='200'):
  return {
    'code': code,
    'data': data,
    'message': message
  }

# 生成token
def generate_token(key, expire=3600):
    ts_str = str(int(time.time()) + expire)
    ts_byte = str(ts_str)
    sha1_tshexstr  = hmac.new(bytes(str(key), 'utf-8'), bytes(ts_byte, 'utf-8')).hexdigest()
    token = ts_str+':'+sha1_tshexstr
    return token

# 获取用户token
def getUserToken (arg):
  openId = arg['openId']
  # sql = 'select * from user where openId="%s"' % (openId)
  results = session.query(t_user).filter(t_user.openId==openId).all()
  if len(results) == 0 :
    results = False
  else:
    results = results[0]
  if not results :
    return ''
  return results.token

# 判断token的有效性
def validToken (token):
  expireTime = int(token.split(':')[0])
  timeNow = time.time()
  print(timeNow)
  print(expireTime)
  if timeNow > expireTime:
    return False
  else:
    return True

# 判断token 是否存在和失效
def getUserByToken (token):
  valid = validToken(token)
  if valid == False :
    return '1'
  else:
      # sql = 'select * from user where token="%s"' % (token)
      results = session.query(t_user).filter(t_user.token==token).all()
      if len(results) == 0 :
        results = '2'
      else:
        results = results[0]

  return results










