#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Float, create_engine, Integer, ForeignKey, Time, BigInteger, Text,DateTime, TIMESTAMP
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# user 用户:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(String(255), primary_key=True)
    name = Column(String(20), comment="昵称")
    openId = Column(String(255), comment="微信openid")
    token = Column(String(255), comment="token")
    phone = Column(String(255), comment="手机号")
    city = Column(String(30), comment="所在城市")
    auth = Column(Integer, comment="认证状态")
    age = Column(Integer, comment="年龄")
    account = Column(String(11), comment="账号，预留字段")
    avatarUrl = Column(String(30), comment="用户头像")

# game 游戏分类:
class Game(Base):
    # 表的名字:
    __tablename__ = 'game'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    logo = Column(String(255), comment="游戏logo")
    name = Column(String(10), comment="游戏名字")

# auth 段位列表:
class Level(Base):
    # 表的名字:
    __tablename__ = 'level'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    gameId = Column(Integer, ForeignKey("game.id"), comment="游戏分类")
    levelName = Column(String(30), comment="段位名称")
    levelImg = Column(String(255), comment="段位图")

# auth 申请认证表:
class Auth(Base):
    # 表的名字:
    __tablename__ = 'auth'

    # 表的结构:
    id = Column(String(255), primary_key=True)
    gameId = Column(Integer, comment="游戏id")
    userId = Column(String(255), ForeignKey("user.id"),comment="用户id")
    voidSrc = Column(String(255), comment="音频路径")
    gameImg = Column(String(255), comment="资质图")
    sex = Column(Integer, comment="性别 1:男；2:女")
    status = Column(Integer, comment="认证状态0:未认证 1:已认证")
    levelId = Column(Integer, ForeignKey("level.id"), comment="段位id")
    detail = Column(String(35), comment="技能介绍")
    ugameId = Column(String(35), comment="认证的游戏id")
    createTime = Column(TIMESTAMP, comment="创建时间")

# activity 发帖列表:
class Activity(Base):
    # 表的名字:
    __tablename__ = 'activity'

    # 表的结构:
    id = Column(String(255), primary_key=True)
    userId = Column(String(255), ForeignKey("user.id"), comment="发贴人")
    createTime = Column(TIMESTAMP, comment="创建时间")
    startTime = Column(TIMESTAMP, comment="发车时间")
    detail = Column(String(200), comment="描述")
    seat = Column(Integer, comment="座位数")
    vacancy = Column(Integer, comment="空位")
    cover = Column(Text, comment="活动海报")
    gameId = Column(Integer, ForeignKey("game.id"), comment="游戏分类")
    user = relationship("User", backref="activity")

# passenger 乘客:
class Passenger(Base):
    # 表的名字:
    __tablename__ = 'passenger'

    # 表的结构:
    id = Column(String(255), primary_key=True)
    userId = Column(String(255), ForeignKey("user.id"), comment="乘客id")
    createTime = Column(TIMESTAMP, comment="申请时间")
    status = Column(Integer, comment="状态: 1: 未同意；2: 已同意；3: 已拒绝")
    activityId = Column(String(255), ForeignKey("activity.id"), comment="活动id")
    detail = Column(String(200), comment="留言")

# message 消息:
class Message(Base):
    # 表的名字:
    __tablename__ = 'message'

    # 表的结构:
    id = Column(String(255), primary_key=True)
    sendId = Column(String(255), ForeignKey("user.id"), comment="消息发送者ID")
    receiveId = Column(String(255), ForeignKey("user.id"), comment="消息接收者Id")
    msg = Column(String(255), comment="消息内容")
    time = Column(TIMESTAMP, comment="消息发送时间")
    msgType = Column(Integer, comment="消息类型 [1聊天；2系统；3上车消息]")
    status = Column(Integer, comment="消息状态: 1:未读；2:已读")

# 评论:
class Comment(Base):
    # 表的名字:
    __tablename__ = 'comment'

    # 表的结构:
    id = Column(String(255), primary_key=True)
    activityId = Column(String(255),  comment="活动id")
    userId = Column(String(255), comment="用户id")
    content = Column(Text, comment="评论内容")
    time = Column(TIMESTAMP, comment="评论时间")
    userAvatarUrl = Column(String(255), comment="用户头像")
    userName = Column(String(255), comment="用户昵称")
    imgs = Column(Text, comment="上传图片")

# 回复表:
class Reply(Base):
    # 表的名字:
    __tablename__ = 'reply'

    # 表的结构:
    id = Column(String(255), primary_key=True)
    activityId = Column(String(255),  comment="活动id")
    userId = Column(String(255), comment="用户id")
    userAvatarUrl = Column(String(255), comment="用户头像")
    userName = Column(String(255), comment="用户昵称")
    parentId = Column(String(255), comment="父级id")
    replyCmtId = Column(String(255), comment="回复的子评论id")
    content = Column(Text, comment="评论内容")
    time = Column(TIMESTAMP, comment="评论时间")
    toId = Column(String(255), comment="回复id")
    toAvatarUrl = Column(String(255), comment="回复头像")
    toName = Column(String(255), comment="回复昵称")

engine = create_engine('mysql+mysqlconnector://root:wts123456@127.0.0.1:3306/pp')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# Base.metadata.create_all(engine)
# 创建session对象:
session = DBSession()
# # 创建新User对象:
# new_user = User(id='5', name='Bob')
# # 添加到session:
# session.add(new_user)
# # 提交即保存到数据库:
# session.commit()
# # 关闭session:
# session.close()

# # 创建Session:
# session = DBSession()
# # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
# user = session.query(User).filter(User.id=='5').one()
# # 打印类型和对象的name属性:
# print('type:', type(user))
# print('name:', user.name)
# # 关闭Session:
# session.close()
