#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from wx.tabels import User as t_user
from wx.tabels import Activity as t_activity
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
from sqlalchemy.orm import scoped_session
print('当前时间')
print(datetime.datetime.now())
# # # 初始化数据库连接:
# engine = create_engine('mysql+mysqlconnector://root:wts123456@127.0.0.1:3306/pp')
# # 创建DBSession类型:
# DBSession = sessionmaker(bind=engine)

# # # 创建Session:
# session = DBSession()
session = ''
print('sql初始化')
class DbMgr(object):
  def __del__(self):
    db.session.close()

  def __init__(self):
    # 初始化数据库连接:
    # self.engine = create_engine('mysql+mysqlconnector://root:wts123456@127.0.0.1:3306/pp', pool_size=5)
    self.engine = create_engine('mysql+mysqlconnector://root:Wts123456@rm-bp1y8030y4sj888225o.mysql.rds.aliyuncs.com:3306/pp', pool_size=5)
    # 创建DBSession类型:
    self.DBSession = sessionmaker(bind=self.engine,  autoflush=False)
    # # 创建Session:
    self.session = scoped_session(self.DBSession)
    session = self.session
    print('数据初始化')

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






