#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from wx.tabels import User as t_user
# from wx import tabels as
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from django.core import serializers

from sqlalchemy.pool import NullPool
from flask_restful import reqparse, fields, marshal
import json
import time
import base64
import hmac
import uuid
import datetime
from wx.tabels import Activity as t_activity
from sqlalchemy.orm import scoped_session
import pendulum

print('当前时间')
print(datetime.datetime.now())
# # # 初始化数据库连接:
# engine = create_engine('mysql+mysqlconnector://root:wts123456@127.0.0.1:3306/pp')
# # 创建DBSession类型:
# DBSession = sessionmaker(bind=engine)

# # # 创建Session:
# session = DBSession()
session = ''

class DbMgr(object):
  def __del__(self):
    db.session.close()

  def __init__(self):
    # 初始化数据库连接:
    # self.engine = create_engine('mysql+mysqlconnector://root:wts123456@127.0.0.1:3306/pp', pool_size=5)
    self.engine = create_engine('mysql+mysqlconnector://root:Wts123456@rm-bp1y8030y4sj888225o.mysql.rds.aliyuncs.com:3306/pp', poolclass=NullPool, echo=False)
    # 创建DBSession类型:
    self.DBSession = sessionmaker(bind=self.engine,  autoflush=False)
    # # 创建Session:
    self.session = scoped_session(self.DBSession)
    session = self.session
    print('数据库链接')
    # time1 = pendulum.now('UTC').float_timestamp * 1000
    # rows = self.session.query(t_game).all()
    # rowsDic = {
    #   'id': fields.Integer(attribute='id'),
    #   'logo': fields.String(attribute='logo'),
    #   'name': fields.String(attribute='name'),
    #   'views': fields.String(attribute='views')
    # }
    # rows =  marshal(rows, rowsDic)
    # self.session.close()
    # time2 = pendulum.now('UTC').float_timestamp * 1000
    # t = time2 - time1
    # t = str(t)
    # print('sql耗时22:::', t)

  def insert(self, row):
    self.session.add(row)
    self.session.commit()
    self.session.close()

  def select(self, row):
    print('select打印')
    try:
      self.session.close()
    except:
      print('select异常')
      self.session.rollback()

  def update(self, row):
    self.session.commit()
    self.session.close()

db = DbMgr()

if __name__ == '__main__':
  session = DbMgr().session
  print(session,'数据库session')






