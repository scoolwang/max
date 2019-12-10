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
from wx.tabels import Words as t_words
import math
# from wx import tabels as
from sqlalchemy import create_engine, func, and_
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
print(sqlConnect.db)
db = sqlConnect.db
# db = sqlConnect.db
session = db.session
engine = db.engine
# 查询活动详情
def activityDetail (arg, userInfo):
  activityId = arg['id']
  results = results = session.query(t_activity, t_user.name, t_user.age, t_user.avatarUrl, t_game.name, t_game.logo, t_auth.sex, t_auth.levelId, t_auth.status, t_level.levelImg, t_user.id).outerjoin(t_auth, and_(t_auth.userId == t_activity.userId, t_auth.gameId==t_activity.gameId)).join(t_user, t_activity.userId == t_user.id).join(t_game, t_activity.gameId==t_game.id).outerjoin(t_level, t_level.id == t_auth.levelId).filter(t_activity.id==activityId)


  # results = session.query(t_activity, t_user.name, t_game.name, t_game.logo).join(t_user, t_activity.userId == t_user.id).join(t_game, t_activity.gameId==t_game.id).all()
  arry = []
  for item, userName, userAge,avatarUrl, gameName, gameLogo, authSex, levelId, authStatus, levelImg,userId in results :
    item.userName = userName
    item.age = userAge
    item.gameName = gameName
    item.gameLogo = gameLogo
    item.sex = authSex
    item.levelId = levelId
    item.auth = authStatus
    item.avatarUrl = avatarUrl
    item.levelImg = levelImg
    # item.startDate = pendulum.instance(item.startTime).float_timestamp
    item.startTime = pendulum.instance(item.startTime).float_timestamp * 1000
    item.createTime = pendulum.instance(item.createTime).float_timestamp * 1000
    arry.append(item)

  dic = {
    'avatarUrl': fields.String, # 用户名    'userId': fields.String, # 用户id
    'id': fields.String, # 活动ID
    'detail': fields.String, # 描述
    'title': fields.String, # 标题
    'gameId': fields.String, # 游戏ID
    'gameName': fields.String, # 游戏名字
    'gameLogo': fields.String, # 游戏图标
    'userName': fields.String, # 用户名
    'userId': fields.String, # 用户id
    'cover': fields.String, # 活动封面
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
  userId = arg.get('userId', False)
  gameId = arg.get('gameId', False)
  filterUserId = userInfo['id']
  # if userId:
  #   filterUserId = userId
  time1 = pendulum.now('UTC').float_timestamp * 1000
  results = session.query(t_activity, t_user.name, t_user.age, t_user.avatarUrl, t_game.name, t_game.logo, t_auth.sex, t_auth.levelId, t_auth.status, t_level.levelImg, t_user.id, t_passenger.id)
  results = results.outerjoin(t_auth, and_(t_auth.userId == t_activity.userId, t_auth.gameId==t_activity.gameId))
  results = results.join(t_user, t_activity.userId == t_user.id)
  results = results.outerjoin(t_passenger, and_(t_passenger.activityId == t_activity.id, t_passenger.userId==filterUserId))
  results = results.join(t_game, t_activity.gameId==t_game.id)
  results = results.outerjoin(t_level, t_level.id == t_auth.levelId)
  results = results.order_by(t_activity.createTime.desc())


  if userId:
    results = results.filter(t_activity.userId==userId)

  if gameId:
    results = results.filter(t_activity.gameId==gameId)

  num = results.count()
  results = results.limit(pageSize).offset(page * pageSize)

  # results = session.query(t_activity, t_user.name, t_game.name, t_game.logo).join(t_user, t_activity.userId == t_user.id).join(t_game, t_activity.gameId==t_game.id).all()
  time2 = pendulum.now('UTC').float_timestamp * 1000
  t = time2 - time1
  t = str(t)
  print('sql查询耗时:', t)
  arry = []
  for item, userName, userAge, avatarUrl, gameName, gameLogo, authSex, levelId, authStatus, levelImg, userId, pid in results :
    if pid == None:
      passenger = 2
    else:
      passenger = 1
    act = {
      'id': item.id, # 活动ID
      'userId': userId, # 用户
      'detail': item.detail, # 描述
      'title': item.title, # 标题
      'gameId': item.gameId, # 游戏ID
      'gameName': gameName, # 游戏名字
      'gameLogo': gameLogo, # 游戏图标
      'userName': userName, # 用户名
      'avatarUrl': avatarUrl, # 用户名    'userId': fields.String, # 用户id
      'cover': item.cover, # 活动封面
      'desc': item.detail, # 描述
      'isPassenger': passenger, # 1已申请，2未申请
      'startTime': pendulum.instance(item.startTime).float_timestamp * 1000, # 发车时间
      # 'startDate': fields.Integer(attribute='startTime'), # 发车时间
      'createTime': pendulum.instance(item.createTime).float_timestamp * 1000, # 发帖时间
      'vacancy': item.vacancy, # 空位
      'seat': item.seat, # 座位总数
      'sex': authSex, # 性别
      'levelId':  levelId, # 段位id
      'auth':  authStatus, # 认证状态
      'age':  userAge, # 年龄
      'levelImg':  levelImg # 段位logo
    }
    arry.append(act)

  time3 = pendulum.now('UTC').float_timestamp * 1000
  t1 = time3 - time2
  t1 = str(t1)

  # session.close()
  print('遍历耗时:', t1)
  return returnFormat(arry, total=num)

# 发布活动
def addActivity (arg, userInfo):
  # startTime = int(arg['startTime'])
  startTime = int(arg['startTime'])
  desc = arg['desc']
  seat = int(arg['seat'])
  # city = arg['city']
  cover = arg['cover']
  gameId = arg['gameId']
  title = arg['title']
  activityId = str(uuid.uuid1())
  # createTime = int(round(time.time() * 1000))
  createTime = pendulum.now('UTC')
  if startTime == '':
    startTime = 0
  else:
    startTime = int(startTime)
    startTime = datetime.datetime.fromtimestamp(startTime/1000)
    startTime = pendulum.instance(startTime)
  userId = userInfo['id']
  results = t_activity(id=activityId, gameId=gameId, cover=cover, detail=desc, title=title, startTime=startTime, createTime=createTime, seat=seat, userId=userId, vacancy=seat)
  session.add(results)
  session.commit()
  session.close()
  # sql = 'insert into activity (id, userId, createTime, startTime, t_desc, t_limit, t_left, cover, gameId) values ("%s", "%s", "%d", "%d", "%s", "%d", "%d", "%s", "%s")' % (activityId, userId, createTime, startTime, desc, limit, 0, cover, gameId)
  # results = runSql(sql)
  return returnFormat(activityId, '发布成功')

# 参加活动
def joinActivity (arg, userInfo):
  ids = str(uuid.uuid1())
  activityId = arg['id']
  detail = arg['detail']

  userId = userInfo['id']
  status = 3
  createTime = pendulum.now('UTC')
  results = session.query(t_passenger).filter(t_passenger.userId==userId, t_passenger.activityId==activityId).all()
  session.close()
  with session.no_autoflush:
    activity = session.query(t_activity, t_user.name, t_user.avatarUrl).join(t_user, t_user.id==t_activity.userId).filter(t_activity.id==activityId).one()
    session.close()
  if len(results) > 0:
    return returnFormat('', '已申请过', '901')

  row = t_passenger(id=ids, activityId=activityId, detail=detail,createTime=createTime,userId=userId, status=status)
  session.add(row)
  session.commit()
  session.close()
  arg = {
    'sendId': userId,
    'receiveId':activity.Activity.userId,
    'time': createTime.format('x'),
    'type': 3,
    'data': {
      'sendName': activity.name,
      'sendAvatar': activity.avatarUrl,
      'content': detail,
      'activityTitle': activity.Activity.title,
      'activityId': activityId
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
  activity = session.query(t_activity).filter(t_activity.id==activityId).first()
  results = session.query(t_passenger,
    t_passenger.detail,
    t_passenger.status,
    t_passenger.createTime,
    t_user.id,
    t_user.name,
    t_user.avatarUrl,
    t_auth.sex,
    t_user.age,
    t_auth.status).join(t_user, t_passenger.userId==t_user.id).outerjoin(t_auth, and_(t_passenger.userId==t_auth.userId, t_auth.gameId==activity.gameId)).filter(t_passenger.activityId==activityId).all()
  arry = []


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

  activity = session.query(t_activity, t_activity.title).filter(t_activity.id==activityId).one()
  if len(parentId) > 0 :
    reply = session.query(t_comment).filter(t_comment.id==parentId).one()
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
    msg = {
      'sendId': userId,
      'receiveId':toId,
      'time': createTime.float_timestamp * 1000,
      'type': 5,
      'id': ids,
      'data': {
        'sendName': userName,
        'sendAvatar': userAvatarUrl,
        'content': content,
        'activityTitle': activity.title,
        'activityId': activityId,
        'replyCmtId': replyCmtId
      }
    }
    if parentId==replyCmtId:
      cmt = session.query(t_comment, t_comment.content).filter(t_comment.id==parentId).one()
    else:
      if toId==userId:
        msg['data']['replyCmtId'] = parentId
        cmt = session.query(t_comment, t_comment.content).filter(t_comment.id==parentId).one()
      else:
        cmt = session.query(t_reply, t_reply.content).filter(t_reply.id==replyCmtId).one()
    msg['data']['replyContent'] = cmt.content
    # if cmt.toId==cmt.userId:
  else:
    # 添加评论
    msg = {
      'sendId': userId,
      'receiveId':activity.Activity.userId,
      'time': createTime.float_timestamp * 1000,
      'type': 5,
      'id': ids,
      'data': {
        'sendName': userName,
        'sendAvatar': userAvatarUrl,
        'content': content,
        'activityTitle': activity.title,
        'activityId': activityId
      }
    }
    addComment = t_comment(id=ids, userId=userId, time=createTime, activityId=activityId, content=content, userName=userName, userAvatarUrl=userAvatarUrl, imgs=imgs)
    db.insert(addComment)

  socket1.sendMsg(msg)
  addMsg(msg)
  return  returnFormat({'id': ids}, '评论成功')

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
  if page >= maxPage :
    return returnFormat([], total=commentTotal.total)

  #评论查询
  comment = session.query(t_comment, t_comment.time, t_comment.id).order_by(t_comment.time.asc()).filter(t_comment.activityId==activityId).limit(pageSize).offset(page * pageSize)

  session.close()
  ids = []

  for item, time, id in comment:
    ids.append(id)

  parentIds = ','.join(map(lambda x: "'%s'" % x, ids))
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
    time = pendulum.instance(item.time).float_timestamp * 1000
    replyItem['time'] = time
    reply.append(replyItem)
    replyObj[parentId] = reply

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
    time = pendulum.instance(item.time).float_timestamp * 1000
    item.time = time
    arry.append(item)

  results =  marshal(arry, replydic)
  db.select(reply)
  return returnFormat(results)

# 获取用户申请加入的帖子
def getMyJoin(arg, userInfo):
  page = int(arg['page']) - 1
  pageSize = int(arg['pageSize'])
  userId = userInfo['id']
  results = session.query(t_passenger, t_activity, t_auth, t_level, t_game, t_user, t_words)
  results = results.join(t_activity, t_activity.id==t_passenger.activityId)
  results = results.outerjoin(t_auth, and_(t_auth.userId == t_passenger.userId, t_auth.gameId== t_activity.gameId))
  results = results.join(t_user, t_passenger.userId == t_user.id)
  results = results.join(t_game, t_activity.gameId==t_game.id)
  results = results.outerjoin(t_level, t_level.id == t_auth.levelId)
  results = results.outerjoin(t_words, t_words.activityId == t_activity.id)
  results = results.order_by(t_passenger.createTime.asc())

  results = results.filter(t_passenger.userId==userId)

  results.limit(pageSize).offset(page * pageSize)
  arry = []
  for item, activity, auth, level, game, user, words  in results :
    startTime  =  pendulum.instance(activity.startTime).float_timestamp * 1000
    nowTime = pendulum.now('UTC').float_timestamp * 1000
    if words == None:
      comment = False
    else:
      comment = True
    if nowTime > startTime :
      if item.status==2 :
        status = 4 # 已完成
      elif item.status == 3 :
        status = 5 # 已过期
      else:
        status = item.status
    else:
      status = item.status
    ret = {
      'comment': comment,
      'passengerId': item.id, # 乘客编号
      'id': activity.id, # 活动ID
      'userId': userId, # 用户
      'detail': activity.detail, # 描述
      'status': status, # 上车状态
      'gameId': activity.gameId, # 游戏ID
      'gameName': game.name, # 游戏名字
      'gameLogo': game.logo, # 游戏图标
      'userName': user.name, # 用户名
      'avatarUrl': user.avatarUrl, # 用户名    'userId': fields.String, # 用户id
      'cover': activity.cover, # 活动封面
      'desc': item.detail, # 乘客留言
      'startTime': pendulum.instance(activity.startTime).float_timestamp * 1000, # 发车时间
      # 'startDate': fields.Integer(attribute='startTime'), # 发车时间
      'createTime': pendulum.instance(activity.createTime).float_timestamp * 1000, # 发帖时间
      'vacancy': activity.vacancy, # 空位
      'seat': activity.seat, # 座位总数
      'sex': auth.sex if auth != None else '' , # 性别
      'levelId':  auth.levelId if auth != None else '', # 段位id
      'auth':  auth.status if auth != None else '', # 认证状态
      'age':  user.age, # 年龄
      'levelImg':  level.levelImg  if level != None else '' # 段位logo
    }
    arry.append(ret)


  session.close()

  return returnFormat(arry)

# 撤回退票
def recallJoin(arg, userInfo):
  passengerId = arg['id']
  activityId = arg['activityId']
  row = session.query(t_passenger).filter(t_passenger.id==passengerId, t_passenger.activityId==activityId).first()
  session.delete(row)

  session.commit()
  session.close()
  return returnFormat('', '撤回成功')

# 评价用户
def commentUser(arg, userInfo):
  activityId = arg['id']
  content = arg['content']
  fromUser = userInfo['id']
  row = session.query(t_activity).filter(t_activity.id==activityId).first()
  toUser = row.userId
  gameId = row.gameId
  ids = str(uuid.uuid1())
  createTime = pendulum.now('UTC')
  addRow = t_words(id=ids, from_user=fromUser, to_user=toUser, content=content, activityId=activityId, gameId=gameId, time=createTime)
  db.insert(addRow)
  return  returnFormat('', '评论成功')

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
#   if userInfo == '1' or userInfo == '2':
#     return returnFormat('', 'token无效', '701')
#   else:
#     userId = userInfo['id']
#     sql = 'insert into auth (id, userId, gameId, voidSrc, gameImg, sex, age) values ("%s", "%s", "%d", "%s", "%s", "%s", "%s")' % (authId, userId, gameId, voidSrc, gameImg, sex, age)
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
#   # userInfo = getUserByToken(token)
#   # if userInfo == '1' or userInfo == '2':
#   #   return returnFormat('', 'token无效', '701')
#   # else:
#   sql = 'insert into message (id, sendId, receiveId, msg, time, type, status) values ("%s", "%s", "%s", "%s", "%d", "%d", "%d")' % (msgId, sendId, receiveId, msg, timeStr, msgType, status)
#   results = runSql(sql)
#   return returnFormat('', '添加成功')

# # 获取未读消息列表
# def getMsg (arg):
#   token = arg['token']
#   userInfo = getUserByToken(token)
#   if userInfo == '1' or userInfo == '2':
#     return returnFormat('', 'token无效', '701')
#   else:
#     userId = userInfo['id']
#     sql = 'select t1.*, t2.name, t2.avatarUrl from message as t1, user as t2 where t1.receiveId= "%s" and t1.status=0 and t2.id=t1.sendId order by t1.time ASC' % (userId)
#     results = runSql(sql)
#     return returnFormat(results, 'success')

# #标记消息为已读状态
# def readChatMsg (arg):
#   sendId = arg['id']
#   token = arg['token']
#   userInfo = getUserByToken(token)
#   if userInfo == '1' or userInfo == '2':
#     return returnFormat('', 'token无效', '701')
#   else:
#     userId = userInfo['id']
#     sql = 'update message set status=1 where receiveId="%s" and sendId="%s"' % (userId, sendId)
#     results = runSql(sql)
#     return returnFormat('', '')

# # 获取用户的未读消息
# def getUnReadMsgByUser (arg):
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









