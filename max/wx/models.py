from contextlib import contextmanager
import pymysql
import json
import time
import base64
import hmac
import uuid
@contextmanager
def mysql(host='127.0.0.1', port=3306, user='root', passwd='wts123456', db='max',charset='utf8'):
  conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
  cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
  try:
    yield cursor
  finally:
    conn.commit()
    cursor.close()
    conn.close()
def runSql (sql):
  with mysql() as cur:
    cur.execute(sql)
    results = cur.fetchall()
    print(results)
  return results

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
  sql = 'select * from user where openId="%s"' % (openId)

  results = runSql(sql)
  if len(results) == 0 :
    results = False
  else:
    results = results[0]
  if not results :
    return ''
  return results['token']

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

# 获取用户信息
def getUser (arg):
  openId = arg['openId']
  tokenGet = arg['token']
  sql = 'select * from user where openId="%s"' % (openId)

  results = runSql(sql)
  if len(results) == 0 :
    results = False
  else:
    results = results[0]

  if not results :
    return returnFormat('', '用户不存在', '901')
  obj = {}
  id = results['id']
  name = results['name']
  token = results['token']
  obj['userId'] = id
  obj['nickName'] = name
  obj['openId'] = results['openId']
  valid = False
  if tokenGet == token :
    valid = validToken(token)
  else:
    return returnFormat('', 'token无效', '701')
  if valid == False :
    return returnFormat('', 'token过期', '701')

  return returnFormat(obj)

# 登录
def login (arg):
  openId = arg['openId']
  # session_key = arg['session_key']
  sql = 'select * from user where openId="%s"' % (openId)
  obj = {}
  results = runSql(sql)
  print(len(results))
  if len(results) == 0 :
    results = False
  else:
    results = results[0]




  if not results :
    return returnFormat('', '登录openId未注册', '901')
  else:
    userId = results['id']
    token = results['token']
    # valid = validToken(token)
    if not token :
      valid = False
    else:
      valid = validToken(token)

    if valid == False:
      token = generate_token(userId)
      # 更新token
      sql = 'update user set token="%s" where openId="%s"' % (token, openId)
      updateResult = runSql(sql)

  obj['userId'] = userId
  obj['nickName'] = results['name']
  obj['openId'] = results['openId']
  obj['token'] = token
  return returnFormat(obj)

# 注册
def register (arg):
  print(arg)
  # regType = arg['regType']
  regAccount = arg['openId']
  name = arg['name']
  userId = str(uuid.uuid1())
  token = generate_token(userId)
  sql = 'insert into user (name, openId, token, id) values ("%s", "%s", "%s", "%s")' % (name, regAccount, token, userId)
  runSql(sql)
  return returnFormat({'token': token, 'userId': userId}, '注册成功')

# 查询所有活动
def activityList (arg):
  sql = 'select t1.*, t2.name, t2.city, t2.level from activity t1 left join user t2 on t1.userId=t2.id'
  results = runSql(sql)
  if len(results) == 0 :
    results = []
  else:
    results = results
  return returnFormat(results)

def getUserByToken (token):
  valid = validToken(token)
  if valid == False :
    return '1'
  else:
      sql = 'select * from user where token="%s"' % (token)
      results = runSql(sql)
      if len(results) == 0 :
        results = '2'
      else:
        results = results[0]

  return results


# 发布活动
def addActivity (arg):
  token = arg['token']
  # startTime = int(arg['startTime'])
  startTime = arg['startTime']
  desc = arg['desc']
  limit = int(arg['limit'])
  city = arg['city']
  cover = arg['cover']
  gameId = arg['gameId']
  activityId = str(uuid.uuid1())
  createTime = time.time()
  userInfo = getUserByToken(token)
  userId = userInfo['id']
  if startTime == '':
    startTime = 0
  else:
    startTime = int(startTime)

  print('*******')
  print(startTime)
  if userInfo == '1' or userInfo == '2':
    return returnFormat('', 'token无效', '701')
  else:
    sql = 'insert into activity (id, userId, createTime, startTime, t_desc, t_limit, t_left, city, cover, gameId) values ("%s", "%s", "%d", "%d", "%s", "%d", "%d", "%s", "%s", "%s")' % (activityId, userId, createTime, startTime, desc, limit, 0, city, cover, gameId)
    print(sql)
    results = runSql(sql)
    return returnFormat('', '发布成功')




















