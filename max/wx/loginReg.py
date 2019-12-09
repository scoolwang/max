#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 模块：登录注册相关

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
from wx.sqlCommon import returnFormat, generate_token, getUserToken, validToken
from wx.aescrypt import EncryptAES

aes = EncryptAES()
db = sqlConnect.db
session = db.session
# 登录
def login (arg):
  openId = arg['openId']
  # session_key = arg['session_key']
  # sql = 'select * from user where openId="%s"' % (openId)
  results = session.query(t_user).filter(t_user.openId==openId).all()

  obj = {}
  # results = runSql(sql)
  # print(len(results))
  if len(results) == 0 :
    results = False
  else:
    results = results[0]

  if not results :
    session.close()
    return returnFormat('', '登录openId未注册', '901')
  else:
    userId = results.id
    token = results.token
    # print('揭秘', token)
    # print('揭秘', openId)
    print(userId, '查询token')
    # valid = validToken(token)
    if not token :
      valid = False
    else:
      tokenValid = aes.decrypt(token)
      # print('登录揭秘', token)
      valid = validToken(tokenValid)

    if valid == False:
      token = generate_token(userId)
      session.query(t_user).filter(t_user.id==userId).update({'token': token})
      try:
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()
      except:
        session.rollback()
        return returnFormat('202', '数据库操作失败')

  obj['userId'] = userId
  obj['name'] = results.name
  obj['avatarUrl'] = results.avatarUrl
  obj['openId'] = results.openId
  obj['token'] = token
  session.close()
  return returnFormat(obj)

# 注册
def register (arg):
  print(arg)
  # regType = arg['regType']
  regAccount = arg['openId']
  avatarUrl = arg['avatarUrl']
  name = arg['name']
  userId = str(uuid.uuid1())
  token = generate_token(userId)
  # sql = 'insert into user (name, openId, token, id) values ("%s", "%s", "%s", "%s")' % (name, regAccount, token, userId)
  results = t_user(name=name, openId=regAccount,avatarUrl=avatarUrl, token=token, id=userId)
  # 添加到session:
  session.add(results)
  # 提交即保存到数据库:
  session.commit()
  # 关闭session:
  session.close()
  return returnFormat({'token': token, 'userId': userId}, '注册成功')









