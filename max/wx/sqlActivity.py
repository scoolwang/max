#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 活动相关

from wx.tabels import User as t_user
from wx.tabels import Activity as t_activity
from wx.tabels import Game as t_game
from wx.tabels import Passenger as t_passenger
from wx.tabels import Auth as t_auth
from wx.tabels import Level as t_level
from wx.tabels import Comment as t_comment
from wx.tabels import Reply as t_reply
import math
# from wx import tabels as
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from django.core import serializers
from flask_restful import reqparse, fields, marshal, marshal_with
import json
import time
import datetime
import base64
import hmac
import uuid
import arrow
import pendulum
from wx import sqlConnect
from wx.sqlCommon import returnFormat, generate_token, getUserToken, validToken, getUserByToken
from wx.sqlMsg import addMsg
from wx import socket1
db = sqlConnect.DbMgr()
session = db.session
engine = db.engine
print('当前时间')
print(datetime.datetime.now())
# 查询活动详情
def activityDetail (arg, userInfo):
  activityId = arg['id']
  results = session.query(t_activity, t_user.name, t_user.age, t_game.name, t_game.logo, t_auth.sex, t_auth.levelId, t_auth.status, t_level.levelImg).join(t_user, t_activity.userId == t_user.id).join(t_game, t_activity.gameId==t_game.id).filter(t_activity.id==activityId).all()
  # results = session.query(t_activity, t_user.name, t_game.name, t_game.logo).join(t_user, t_activity.userId == t_user.id).join(t_game, t_activity.gameId==t_game.id).all()
  print(len(results), '长度')
  arry = []
  for item, userName, userAge, gameName, gameLogo, authSex, levelId, authStatus, levelImg in results :
    print('结果遍历', item.startTime)
    item.userName = userName
    item.age = userAge
    item.gameName = gameName
    item.gameLogo = gameLogo
    item.sex = authSex
    item.levelId = levelId
    item.auth = authStatus
    item.levelImg = levelImg
    item.startDate = time.mktime(item.startTime.timetuple()) * 1000
    item.startTime = arrow.get(item.startTime).timestamp * 1000
    item.createTime = arrow.get(item.createTime).timestamp * 1000
    arry.append(item)

  dic = {
    'id': fields.String, # 活动ID
    'detail': fields.String, # 描述
    'gameId': fields.String, # 游戏ID
    'gameName': fields.String, # 游戏名字
    'gameLogo': fields.String, # 游戏图标
    'userName': fields.String, # 用户名
    'userId': fields.String, # 用户id
    'cover': fields.String, # 活动封面
    'desc': fields.String(attribute='detail'), # 描述
    'startTime': fields.Integer, # 发车时间
    'createTime': fields.Integer, # 发帖时间
    'vacancy': fields.String, # 空位
    'seat': fields.String, # 座位总数
    'sex': fields.String, # 性别
    'levelId':  fields.String, # 段位id
    'auth':  fields.String, # 认证状态
    'age':  fields.String, # 年龄
    'levelImg':  fields.String # 段位logo
  }

  results =  marshal(arry, dic)
  session.close()
  print('活动', results)
  if len(results) == 0 :
    results = []
  else:
    results = results
  # db.select(results)
  return returnFormat(results[0])
# 查询所有活动
def activityList (arg, userInfo):
  page = int(arg['page']) - 1
  pageSize = int(arg['pageSize'])

  results = session.query(t_activity, t_user.name, t_user.age, t_user.avatarUrl, t_game.name, t_game.logo, t_auth.sex, t_auth.levelId, t_auth.status, t_level.levelImg).join(t_user, t_activity.userId == t_user.id).join(t_game, t_activity.gameId==t_game.id).limit(pageSize).offset(page * pageSize)
  # results = session.query(t_activity, t_user.name, t_game.name, t_game.logo).join(t_user, t_activity.userId == t_user.id).join(t_game, t_activity.gameId==t_game.id).all()

  arry = []
  for item, userName, userAge, avatarUrl, gameName, gameLogo, authSex, levelId, authStatus, levelImg in results :
    print('结果遍历', item.startTime)
    item.userName = userName
    item.age = userAge
    item.gameName = gameName
    item.avatarUrl = avatarUrl
    item.gameLogo = gameLogo
    item.sex = authSex
    item.levelId = levelId
    item.auth = authStatus
    item.levelImg = levelImg
    item.startDate = time.mktime(item.startTime.timetuple()) * 1000
    item.startTime = arrow.get(item.startTime).timestamp * 1000
    item.createTime = arrow.get(item.createTime).timestamp * 1000
    arry.append(item)

  dic = {
    'id': fields.String, # 活动ID
    'detail': fields.String, # 描述
    'gameId': fields.String, # 游戏ID
    'gameName': fields.String, # 游戏名字
    'gameLogo': fields.String, # 游戏图标
    'userName': fields.String, # 用户名
    'avatarUrl': fields.String, # 用户名    'userId': fields.String, # 用户id
    'cover': fields.String, # 活动封面
    'desc': fields.String(attribute='detail'), # 描述
    'startTime': fields.Integer, # 发车时间
    # 'startDate': fields.Integer(attribute='startTime'), # 发车时间
    'createTime': fields.Integer, # 发帖时间
    'vacancy': fields.String, # 空位
    'seat': fields.String, # 座位总数
    'sex': fields.String, # 性别
    'levelId':  fields.String, # 段位id
    'auth':  fields.String, # 认证状态
    'age':  fields.String, # 年龄
    'levelImg':  fields.String # 段位logo
  }
  results =  marshal(arry, dic)
  print('活动', results)
  session.close()
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
  # createTime = int(round(time.time() * 1000))
  createTime = datetime.datetime.now()
  print('时间', createTime)
  if startTime == '':
    startTime = 0
  else:
    startTime = int(startTime)
    startTime = datetime.datetime.fromtimestamp(startTime/1000)
    print('时间戳转换', startTime)
  userId = userInfo['id']
  results = t_activity(id=activityId, gameId=gameId, cover=cover, detail=desc, startTime=startTime, createTime=createTime, seat=seat, userId=userId, vacancy=seat)
  session.add(results)
  session.commit()
  session.close()
  # sql = 'insert into activity (id, userId, createTime, startTime, t_desc, t_limit, t_left, cover, gameId) values ("%s", "%s", "%d", "%d", "%s", "%d", "%d", "%s", "%s")' % (activityId, userId, createTime, startTime, desc, limit, 0, cover, gameId)
  print(results)
  # results = runSql(sql)
  return returnFormat('', '发布成功')

# 参加活动
def joinActivity (arg, userInfo):
  ids = str(uuid.uuid1())
  activityId = arg['id']
  detail = arg['detail']

  userId = userInfo['id']
  status = 3
  createTime1 = time.time()
  createTime = datetime.datetime.now()
  print('时间', userId, createTime1 * 1000)
  results = session.query(t_passenger).filter(t_passenger.userId==userId, t_passenger.activityId==activityId).all()
  session.close()
  # print(str(session.query(t_passenger).filter(t_passenger.userId==userId)))
  with session.no_autoflush:
    activity = session.query(t_activity, t_user.name, t_user.avatarUrl).join(t_user, t_user.id==t_activity.userId).filter(t_activity.id==activityId).one()
    session.close()
  if len(results) > 0:
    return returnFormat('', '已申请过', '901')

  print(createTime, 'createTime字符串')
  # print(activity.Activity.userId, 'createTime字符串')
  row = t_passenger(id=ids, activityId=activityId, detail=detail,createTime=createTime,userId=userId, status=status)
  session.add(row)
  session.commit()
  session.close()
  arg = {
    'sendId': userId,
    'receiveId':activity.Activity.userId,
    'time': createTime1 * 1000,
    'type': 3,
    'data': {
      'sendName': activity.name,
      'sendAvatar': activity.avatarUrl,
      'content': '加入车队'
    }
  }
  socket1.sendMsg(arg)
  addMsg(arg)
  return returnFormat('', '参加成功')
  # except:
  #     session.rollback()
  #     return returnFormat('202', '数据库操作失败')

# 获取参加成员
def getActivityUsers (arg, userInfo):
  activityId = arg['id']
  results = session.query(t_passenger,
    t_passenger.detail,
    t_passenger.status,
    t_passenger.createTime,
    t_user.id,
    t_user.name,
    t_user.avatarUrl,
    t_auth.sex,
    t_user.age,
    t_auth.status).join(t_user, t_passenger.userId==t_user.id).outerjoin(t_auth, t_passenger.userId==t_auth.id).filter(t_passenger.activityId==activityId).all()
  arry = []
  print(len(results), '用户长度')

  for item, detail, status, createTime, userId, userName, userAvatarUrl, userSex, userAge,authstatus in results :
    item.userName = userName
    item.age = userAge if authstatus== 1 else ''
    item.avatarUrl = userAvatarUrl
    item.sex = userSex if authstatus== 1 else ''
    item.userId = userId
    item.detail = detail
    item.status = status
    item.createTime = arrow.get(item.createTime).timestamp * 1000
    arry.append(item)

  dic = {
    'detail': fields.String, # 描述
    'userName': fields.String, # 用户名
    'userId': fields.String, # 用户id
    'avatarUrl': fields.String, # 活动封面
    'createTime': fields.Integer, # 发帖时间
    'sex': fields.String, # 性别
    'age':  fields.String, # 段位id
    'age':  fields.String, # 年龄
    'status':  fields.String # 请求状态
  }
  session.close()
  results =  marshal(arry, dic)
  # db.select(results)
  return returnFormat(results)

# 修改乘客状态
def editStatus (arg, userInfo):
  userId = arg['userId']
  activityId = arg['activityId']
  status = int(arg['status'])
  actionUserid = userInfo['id']
  activity = session.query(t_activity).filter(t_activity.id==activityId).one()
  session.close()
  print(activity.userId)
  if activity.userId != actionUserid:
    return returnFormat('', '没有权限', '901')

  row = session.query(t_passenger).filter(t_passenger.userId==userId, t_passenger.activityId==activityId).update({'status': status})
  session.commit()
  session.close()
  session.query(t_activity).filter(t_activity.id==activityId).update({'vacancy': activity.seat-1})
  session.commit()
  session.close()
  return returnFormat('', '操作成功')

# 添加评论
def addComment (arg, userInfo):
  ids = str(uuid.uuid1())
  activityId = arg['activityId']
  userId = userInfo['id']
  content = arg['content']
  parentId = arg['parentId'] #回复评论的id
  toId = arg.get('toId', '')
  replyCmtId = arg.get('replyCmtId', '')
  userName = userInfo['name']
  userAvatarUrl = userInfo['avatarUrl']
  imgs = arg['imgs']
  toName = ''
  toAvatarUrl = ''
  createTime = pendulum.now('UTC')

  print('创建时间')
  print(createTime, createTime.timezone_name)
  if len(parentId) > 0 :
    # data = {
    #   'userId': userId,
    #   'content': content,
    #   'parentId': parentId,
    #   'toId': toId,
    #   'userName': userInfo['name'],
    #   'userAvatarUrl': userInfo['avatarUrl']
    # }
    # 添加回复
    toInfo = session.query(t_user, t_user.name, t_user.avatarUrl).filter(t_user.id==toId).one()
    db.select(toInfo)
    toName = toInfo.name
    toAvatarUrl =  toInfo.avatarUrl
    addReply = t_reply(id=ids, userId=userId, time=createTime, activityId=activityId, parentId=parentId, content=content, userName=userName, userAvatarUrl=userAvatarUrl, toId = toId, toAvatarUrl=toAvatarUrl, toName=toName, replyCmtId=replyCmtId)
    db.insert(addReply)
  else:
    # 添加评论
    print('参数')
    print(createTime)
    addComment = t_comment(id=ids, userId=userId, time=createTime, activityId=activityId, content=content, userName=userName, userAvatarUrl=userAvatarUrl, imgs=imgs)
    db.insert(addComment)

  return  returnFormat('', '评论成功')

# 获取评论列表
def getComment(arg, userInfo):
  page = arg.get('page', 1)
  page = int(page) -  1
  pageSize = arg.get('pageSize', 10)
  pageSize = int(pageSize)
  activityId = arg['activityId']

  # 评论总数查询
  commentTotalSql = 'SELECT count(*) as total from comment where activityId="%s"' % (activityId)
  commentTotal = session.execute(commentTotalSql).fetchone()
  cmtTotal = commentTotal.total
  session.close()

  maxPage = math.ceil(cmtTotal/pageSize)
  print(page, maxPage)
  if page >= maxPage :
    return returnFormat([], total=commentTotal.total)

  print('return最后')
  #评论查询
  comment = session.query(t_comment, t_comment.time, t_comment.id).order_by(t_comment.time.asc()).filter(t_comment.activityId==activityId).limit(pageSize).offset(page * pageSize)

  print(comment)
  session.close()
  ids = []

  for item, time, id in comment:
    ids.append(id)

  parentIds = ','.join(map(lambda x: "'%s'" % x, ids))
  print(len(ids), '拼了长度')
  # 回复查询
  sql = "SELECT t.* FROM (SELECT a.*, a.parentId as pId, IF (@str1 = a.parentId, @rank := @rank + 1, @rank := 1) AS rank_no, (@str1 := a.parentId) as d FROM ( SELECT reply.* FROM reply ORDER BY parentId, time asc) a, (select @str1 :=0, @rank :=0) tmp ) t WHERE t.parentId in (%s) and t.rank_no <= 4" % (parentIds)

  totals = 'SELECT parentId, count(1)  as counts from reply  where parentId in (select parentId from reply where activityId="%s") group by parentId' % (activityId)

  totals = session.execute(totals).fetchall()
  arry = []
  totalsObj = {}
  for item in totals :
    totalsObj[item.parentId] = item.counts
  session.close()

  ret = session.execute(sql).fetchall()

  replydic = {
    'activityId': fields.String,
    'id': fields.String,
    'content': fields.String,
    'userId': fields.String,
    'userAvatarUrl': fields.String,
    'userName': fields.String,
    'parentId': fields.String,
    'toId': fields.String,
    'toAvatarUrl': fields.String,
    'toName': fields.String,
    'time': fields.Integer,
    'replyCmtId': fields.String
    # 'reply': fields.List
  }
  replyObj = {}
  print('id                                    内容                              rank_no')
  for item in ret :
    replyItem = {
      'activityId': item.activityId,
      'id': item.id,
      'content': item.content,
      'userId': item.userId,
      'userAvatarUrl': item.userAvatarUrl,
      'userName': item.userName,
      'parentId': item.parentId,
      'toId': item.toId,
      'toAvatarUrl': item.toAvatarUrl,
      'toName': item.toName,
      'replyCmtId': item.replyCmtId
      # 'reply': fields.List
    }
    parentId = item.parentId
    reply = replyObj.get(parentId, [])
    time = pendulum.instance(item.time).format('x')
    replyItem['time'] = time
    reply.append(replyItem)
    replyObj[parentId] = reply
    print(item.parentId, '         ' ,item.content, '                       ', item.rank_no )

  for item, time, id in comment:
    commentId = item.id
    replyList = []
    tt = time
    tt = pendulum.instance(time)
    item.reply = replyObj.get(commentId, [])
    item.time = tt.format('x')
    item.replyTotal = totalsObj.get(commentId, 0) - len(item.reply)
    arry.append(item)

  dic = {
    'activityId': fields.String,
    'id': fields.String,
    'content': fields.String,
    'userId': fields.String,
    'userAvatarUrl': fields.String,
    'userName': fields.String,
    'imgs': fields.String,
    'time': fields.Integer,
    'replyTotal': fields.Integer,
    'reply': fields.Nested(replydic)
  }

  results =  marshal(arry, dic)
  session.close()
  return returnFormat(results, total=commentTotal.total)


# 获取回复列表
def getReply(arg, userInfo):
  commentId = arg['commentId']
  reply = session.query(t_reply).filter(t_reply.parentId==commentId).order_by(t_reply.time.asc()).all()
  replydic = {
    'activityId': fields.String,
    'id': fields.String,
    'content': fields.String,
    'userId': fields.String,
    'userAvatarUrl': fields.String,
    'userName': fields.String,
    'parentId': fields.String,
    'toId': fields.String,
    'toAvatarUrl': fields.String,
    'toName': fields.String,
    'time': fields.Integer,
    'replyCmtId': fields.String
  }
  arry = []
  for item in reply :
    time = pendulum.instance(item.time).format('x')
    item.time = time
    arry.append(item)

  results =  marshal(arry, replydic)
  db.select(reply)
  return returnFormat(results)
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









