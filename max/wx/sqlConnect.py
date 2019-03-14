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
# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:wts123456@127.0.0.1:3306/pp')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# # 创建Session:
session = DBSession()

print('sql初始化')










