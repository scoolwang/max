# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag
import qiniu.config

#需要填写你的 Access Key 和 Secret Key
access_key = 'woOKzcAjAiIWkXjFHmIeLcUTSyr0JVbwPCfCQZqD'
secret_key = 'G3Dwrqhvs4KA7zIgixd3p5zJxMIu0F--gKWDn_4P'

#构建鉴权对象
q = Auth(access_key, secret_key)

#要上传的空间
#图片上传空间名
bucket_name = 'ppgame'
#音频上传空间名
void_name = 'ppgame'


def upload (localfile):
  # putolicy = {
  #   "callbackUrl": "http://t2.kaistart.net/ecommerce/mall/page/get",
  #   "callbackBody": "name=$(fname)&hash=$(etag)&location=$(x:location)&price=$(x:price)"
  # }
  token = q.upload_token(bucket_name, None, 3600)

  return {'uptoken': token}

def uploadVoid (localfile):

  token = q.upload_token(void_name, None, 3600)

  return {'uptoken': token}

def load (arg):
  return {'a': '你好'}
