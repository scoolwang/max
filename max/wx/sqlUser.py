#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 用户相关

from wx.tabels import User as t_user
from wx.tabels import Activity as t_activity
from wx.tabels import Game as t_game
from wx.tabels import Auth as t_auth
from wx.tabels import Level as t_level
from wx.tabels import Fans as t_fans
from wx.tabels import Words as t_words
# from wx import tabels as
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from django.core import serializers
from wx.sqlMsg import addMsg
from flask_restful import reqparse, fields, marshal
import json
import time
import base64
import hmac
import uuid
import pendulum
from wx import socket1
# from wx.sqlConnect import session
from wx import sqlConnect
from wx.sqlCommon import returnFormat, generate_token, getUserToken, validToken, getUserByToken
db = sqlConnect.db
session = db.session

# 获取用户信息
def getUser (arg, userInfo):
  return returnFormat(userInfo)

# 根据id获取用户信息
def getUserById (arg, userInfo):
  print('用户信心token', userInfo)
  userId = arg['userId']
  myUserId = userInfo['id']
  isfans = False
  # sql2 = 'select * from user where id="%s"' % (userId)
  results = session.query(t_user).filter(t_user.id==userId).all()
  fans = session.query(t_fans).filter(t_fans.from_user==myUserId, t_fans.to_user==userId).all()
  fansNum = session.query(t_fans).filter(t_fans.to_user==userId).all()
  fansNum = len(fansNum)
  if len(fans) > 0:
    isfans = True
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
      'age': fields.String,
      'motto': fields.String,
      'isFans': fields.Boolean,
      'fansNum': fields.Integer
    }
    for item in results:
      print('用户信息', item.id)
      item.isFans = isfans
      item.fansNum = fansNum
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
  ret = session.query(t_game, t_auth.status).outerjoin(t_auth,  and_(t_auth.gameId==t_game.id, t_auth.userId==userId))
  print(ret,  '我们')
  dic = {
    'gameId': fields.String,
    'logo': fields.String,
    'gameName': fields.String,
    'status': fields.Integer
  }
  arry = []
  for item, status in ret:
    s = 0 if not status else status
    print(s,  '状态')
    row = {
      'gameId': item.id,
      'logo': item.logo,
      'gameName': item.name,
      'status': s
    }
    arry.append(row)
  results =  marshal(arry, dic)
  return returnFormat(results)

# 更新用户信息
def updateUser(arg, userInfo):
  arg.pop('clientType')
  arg.pop('deviceId')
  person = session.query(t_user).filter(t_user.id==userInfo['id']).update(arg)

  session.commit()
  session.close()
  return returnFormat('')

# 获取用户认证信息
def userAuth(arg, userInfo):
  gameId = int(arg['gameId'])
  userId = arg['userId']
  authList = session.query(t_game, t_auth, t_level, t_user).outerjoin(t_auth, t_game.id==t_auth.gameId).join(t_user, t_user.id==t_auth.userId).join(t_level, and_(t_level.gameId==t_auth.gameId, t_level.id==t_auth.levelId)).filter(t_auth.userId==userId, t_auth.gameId==gameId)
  print(authList)
  authList = authList.all()
  arry = []
  for game, auth, level, user in authList:
    item = {
      'userId': auth.userId,
      'id': auth.id,
      'status': auth.status,
      'voidSrc': auth.voidSrc,
      'voidTime': auth.voidTime,
      'gameImg': auth.gameImg,
      'gameName': game.name,
      'sex': auth.sex,
      'levelId': auth.levelId,
      'levelName': level.levelName,
      'levelImg': level.levelImg,
      'detail': auth.detail,
    }
    arry.append(item)

  if len(authList) <= 0:
    return returnFormat('', '用户未认证该游戏')
  else:
    return returnFormat(arry[0])

# 关注用户
def careUser(arg, userInfo):
  to_user = arg['userId']
  from_user = userInfo['id']
  fans = session.query(t_fans).filter(t_fans.from_user==from_user, t_fans.to_user==to_user).all()
  if len(fans) > 0:
    session.delete(fans[0])
    session.commit()
    session.close()
    return returnFormat('', '已取消关注')

  id = str(uuid.uuid1())
  row = t_fans(id=id, from_user=from_user, to_user=to_user)
  db.insert(row)
  createTime = pendulum.now('UTC')
  msg = {
    'sendId': from_user,
    'receiveId':to_user,
    'time': createTime.float_timestamp * 1000,
    'type': 4,
    'data': {
      'sendName': userInfo['name'],
      'sendAvatar': userInfo['avatarUrl'],
      'content': '',
    }
  }
  socket1.sendMsg(msg)
  addMsg(msg)
  return returnFormat('', '关注成功')

# 获取用户已认证的游戏信息
def userAuthGame(arg, userInfo):
  userId = arg['userId']
  authList = session.query(t_auth, t_game,  t_level, t_user)
  authList = authList.outerjoin(t_game, t_game.id==t_auth.gameId)
  authList = authList.join(t_user, t_user.id==t_auth.userId)
  authList = authList.join(t_level, and_(t_level.gameId==t_auth.gameId, t_level.id==t_auth.levelId))
  authList = authList.filter(t_auth.userId==userId, t_auth.status==1)
  print(authList)
  authList = authList.all()
  arry = []
  for auth, game, level, user in authList:
    item = {
      'userId': auth.userId,
      'id': auth.id,
      'status': auth.status,
      'voidSrc': auth.voidSrc,
      'voidTime': auth.voidTime,
      'gameImg': auth.gameImg,
      'gameId': auth.gameId,
      'gameName': game.name,
      'gameLogo': game.logo,
      'sex': auth.sex,
      'levelId': auth.levelId,
      'levelName': level.levelName,
      'levelImg': level.levelImg,
      'detail': auth.detail,
    }
    arry.append(item)
  db.select(authList)
  return returnFormat(arry)

# 获取用户评价
def getWords(arg, userInfo):
  gameId = arg['gameId']
  userId = arg['userId']
  row = session.query(t_words, t_user).join(t_user, t_user.id==t_words.from_user).filter(t_words.gameId==gameId, t_words.to_user==userId).all()
  arry = []
  for words, user in row:
    item = {
      'id': words.id,
      'userId': words.from_user,
      'to_user': words.to_user,
      'activityId': words.activityId,
      'content': words.content,
      'gameId': words.gameId,
      'userName': user.name,
      'avatarUrl': user.avatarUrl,
      'time': pendulum.instance(words.time).float_timestamp * 1000, # 发帖时间
    }
    arry.append(item)
  db.select(row)
  return returnFormat(arry)

# 获取粉丝
def getFansList(arg, userInfo):
  userId = arg['userId']
  fansNum = session.query(t_fans, t_user).join(t_user, t_user.id==t_fans.from_user).filter(t_fans.to_user==userId).all()
  arry = []
  for fans, user in fansNum:
    item = {
      'userId': user.id,
      'id': fans.id,
      'avatarUrl': user.avatarUrl,
      'name': user.name,
      'motto': user.motto
    }
    arry.append(item)
  session.close()
  return returnFormat(arry)

# 我关注的
def getCareList(arg, userInfo):
  userId = arg['userId']
  fansNum = session.query(t_fans, t_user).join(t_user, t_user.id==t_fans.to_user).filter(t_fans.from_user==userId).all()
  arry = []
  for fans, user in fansNum:
    item = {
      'userId': user.id,
      'id': fans.id,
      'avatarUrl': user.avatarUrl,
      'name': user.name,
      'motto': user.motto
    }
    arry.append(item)
  session.close()
  return returnFormat(arry)

