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
from wx import sqlConnect
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from wx.aescrypt import EncryptAES
db = sqlConnect.db
session = db.session
aes = EncryptAES()
def returnFormat (data, message='', code='200', total=''):
  return {
    'code': code,
    'data': data,
    'message': message,
    'total': total
  }

# 生成token
def generate_token(key, expire=3600):
    ts_str = str((int(time.time()) + expire)* 1000)
    ts_byte = str(ts_str)
    sha1_tshexstr  = hmac.new(bytes(str(key), 'utf-8'), bytes(ts_byte, 'utf-8')).hexdigest()
    token = ts_str+':'+sha1_tshexstr
    print('存储加密钱', token)
    token = aes.encrypt(token)
    print('存储加密后', token)
    return token

# 获取用户token
def getUserToken (arg):
  openId = arg['openId']
  # sql = 'select * from user where openId="%s"' % (openId)
  results = session.query(t_user).filter(t_user.openId==openId).all()
  dic = {
    'age': fields.String,
    'auth': fields.String,
    'avatarUrl': fields.String,
    'city': fields.String,
    'id': fields.String,
    'name': fields.String,
    'phone': fields.String
  }

  if len(results) == 0 :
    results = False
  else:
    token = results[0]
    print(results)
  if not results :
    return ''
  session.close()
  print(results)
  return token

# 判断token的有效性
def validToken (token):
  expireTime = int(token.split(':')[0])
  timeNow = time.time()
  # print(timeNow)
  # print(expireTime)
  if timeNow > expireTime:
    return False
  else:
    return True

# 判断token 是否存在和失效
def getUserByToken (token, openId):  # print('header token', token)
  token = aes.decrypt(token)
  # print('解密后的token', token)
  token = token.split(openId)[1]
  tokenValid = aes.decrypt(token)
  # print('去除openId的token', token)
  # print('tokenValid', tokenValid)
  # valid = False
  valid = validToken(tokenValid)
  print('解析', token)
  # print(valid)
  if valid == False :
    return '1'
  else:
      # sql = 'select * from user where token="%s"' % (token)
      results = session.query(t_user).filter(t_user.token==token).all()
      # db.select(results)

      if len(results) == 0 :
        results = '2'
      else:
        arry = []
        results = results
        dic = {
          'id': fields.String,
          'name': fields.String,
          'openId': fields.String,
          'motto': fields.String,
          # 'token': fields.String,
          'phone': fields.String,
          'city': fields.String,
          'auth': fields.String,
          'avatarUrl': fields.String,
          'age': fields.String
        }
        for item in results:
          arry.append(item)
        results =  marshal(arry, dic)
      session.close()
        # print('用户id', results[0])
  return results[0]










