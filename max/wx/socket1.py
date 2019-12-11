#-*- coding:utf8 -*-

import threading
import hashlib
import socket
import base64
import struct
import json
import time
from wx.sqlMsg import addMsg
chatSocket = {}
chatSendMap = {}
systemSocket = {}
systemSendMap = {}
#通知客户端
def notify(message, connection):
  # for connection in clients.values():
  # data = "need to send messages中文"
  data = message
  token = b'\x81'
  length = len(data.encode())
  if length<=125:
    token += struct.pack('B', length)
  elif length <= 0xFFFF:
    token += struct.pack('!BH', 126, length)
  else:
    token += struct.pack('!BQ', 127, length)
  data = token + data.encode()
  print(data)
  # connection.send('%c%c%s' % (0x81, len(message), message))
  connection.send(data)

def on():
  server1 = websocket_server(9000, chatSocket)
  server1.start()
  server2 = websocket_server(7000, systemSocket)
  server2.start()

def sendMsg(data):
  print('系统池', systemSocket)
  print('系统池', data)
  toid = data['receiveId']
  print('id', toid)
  systemClient = systemSocket.get('id' + toid)
  if not systemClient:
    print('未连接')
  else:
    print('聊天链接' + toid + '')
    message = json.dumps(data)
    notify(message, systemClient)

#客户端处理线程
class websocket_thread(threading.Thread):
    def __init__(self, connection, username, clients, sendMap, port):
        super(websocket_thread, self).__init__()
        print(connection.getpeername())
        self.connection = connection
        self.clients = clients
        self.sendMap = sendMap
        self.username = username
        self.port = str(port)
        print('客户端初始化', self.username)
        print('客户端集合', self.clients)
    def run(self):
        print('新的客户端加入', self.username)
        data = self.connection.recv(1024)
        headers = self.parse_headers(data)
        token = self.generate_token(headers['Sec-WebSocket-Key'])
        print('headers数据')
        print(data)
        str2 = 'HTTP/1.1 101 Switching Protocols \r\n' \
                'Upgrade: WebSocket\r\n'\
                'Connection: Upgrade\r\n'\
                'Sec-WebSocket-Accept: %s\r\n\r\n' % token
        str2 = str2.encode('utf8')
        sendMapKey = 'id'+ headers['data']['sendId']
        self.clients[sendMapKey] = self.connection
        # self.sendMap[sendMapKey] = self.username
        self.connection.send(str2)
        print('新的客户端加入-' + self.port, self.clients)
        while True:
            try:
                data = self.connection.recv(1024)
                print(data)
            except Exception as e:
                print("数据返回异常: ", e)
                self.clients.pop(self.username)
                break
            if not data:
                return
            receiveId = 'id' + headers['data']['receiveId']
            sendId = 'id' + headers['data']['sendId']
            print('系统池', systemSocket)
            print('聊天池', chatSocket)
            # toSocketId = self.sendMap.get(receiveId)
            # fromSocketId = self.sendMap.get(sendId)
            print('客户端发送数据')
            print(data)
            print('clients数据')
            print(self.clients)
            print('sendMap')
            print(self.sendMap)
            data = self.parse_data(data)
            selectClient = self.clients.get(receiveId)
            #客户端关闭连接，解析错误，服务端关闭连接
            if data == 'q':
                print('解析异常，关闭客户端连接')
                selectClient = self.clients.get(sendId)
                selectClient.close()
                del self.clients[sendId]
                return
            message = json.loads(data)
            sqlData = {
                'sendId': headers['data']['sendId'],
                'receiveId': headers['data']['receiveId'],
                'type': 1,
                'time': time.time() * 1000,
                'data': message['data']
            }
            message = json.dumps(sqlData)
            # print('[42m接受的data数据', message['data']['conent'])
            if not selectClient or not data:
                if not selectClient:
                    systemClient = systemSocket.get(receiveId)
                    if not systemClient:
                      print('聊天对象未打开小程序')
                    else:
                      print('聊天对象不在线，系统通知')
                      notify(message, systemClient)
                    addMsg(sqlData)
            else:
                print('[42m服务端转发数据', message)
                print('[42msocket通信id', receiveId)
                notify(message, selectClient)

    # def parse_data(self, msg):
    #   if len(msg) == 0:
    #       return  ''

    #   # 去除二进制中的第1位
    #   v = msg[1] & 0x7f

    #   # p 掩码的开始位

    #   # 1位如果是 126 表接下来的两个字节才是长度
    #   # 接下来两个是长度，加上0位和1位，就是 4 位开始掩码
    #   if v == 0x7e:
    #       p = 4

    #   # 1位 127 表接下来的八个字节才是长度
    #   # 接下来 8 个代表长度，加上 0 and 1 则是 10 开始掩码
    #   elif v == 0x7f:
    #       p = 10

    #   # 1 位 1-125 则本身代表长度
    #   # 0 and 1 则 2 开始掩码
    #   else:
    #       p = 2

    #   # mark 掩码为包长之后的 4 个字节
    #   mask = msg[p:p + 4]
    #   data = msg[p + 4:]
    #   print('解析数据2 \n %s' % data)
    #   print('解析数据3 \n %s' % mask)
    #   #print 'mask num is \n %s' % [ord(v) for v in mask]

    #   #print 'mask little num is \n %s' % [ord(v) & 0x7f for v in mask]

    #   #print 'mask is \n %s' % [chr(ord(v) & 0x7f) for v in mask]
    #   ori = ''
    #   for i, d in enumerate(data):
    #     print('解析', i, d, chr(d ^ mask[i % 4]))
    #     ori += chr(d ^ mask[i % 4])
    #     print('桌布解析', ori)
    #   # ori2 = ''.join([(v ^ mask[k % 4]) for k, v in enumerate(data)])

    #   print('解析数据 \n %s' % ori)
    #   # print('解析数据 \n %s' % ori2)

    #   return ori

    def parse_data(self, info):
        print('第一位', info[1])
        code_len = info[1] & 0x7f
        if code_len == 0x7e:
            extend_payload_len = info[2:4]
            mask = info[4:8]
            decoded = info[8:]
            print('4位')
        elif code_len == 0x7f:
            extend_payload_len = info[2:10]
            mask = info[10:14]
            decoded = info[14:]
            print('10位')
        else:
            extend_payload_len = None
            mask = info[2:6]
            decoded = info[6:]
            print('0位')
        bytes_list = bytearray()
        print('返回的数据12', decoded, len(decoded))
        for i in range(len(decoded)):
            chunk = decoded[i] ^ mask[i % 4]
            bytes_list.append(chunk)
        print('返回的数据1', bytes_list)
        try:
          raw_str = str(bytes_list, encoding="utf-8")
        except Exception as e:
          print('解析异常', e)
          raw_str = 'q'

        print('返回的数据')
        print(raw_str)
        return raw_str

    def parse_headers(self, msg):
        headers = {}
        params = {}
        msg = str(msg, encoding = "utf-8")
        print('msg')
        header, data = msg.split('\r\n\r\n', 1)
        data = header.split('\r\n')[0]
        print(data.split(' ')[1])
        url = data.split(' ')[1].split('?')[1].split('&')
        for arg in url:
            key, value = arg.split('=', 1)
            params[key] = value
        for line in header.split('\r\n')[1:]:
            key, value = line.split(': ', 1)
            headers[key] = value
        headers['data'] = params
        return headers

    def generate_token(self, msg):
        print('msg数据')
        print(msg)
        key = msg + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        key = key.encode('utf8')
        # print('key等他的')
        # print(key.encode('utf8'))
        # key = str(key)
        print(key)
        ser_key = hashlib.sha1(key).digest()
        # ser_key = str(ser_key)
        # print('加密后')
        ser_key = base64.b64encode(ser_key)
        ser_key = ser_key.decode('utf8')
        print(ser_key)
        return ser_key

#服务端
class websocket_server(threading.Thread):
    def __init__(self, port, clients):
        super(websocket_server, self).__init__()
        self.port = port
        self.clients = clients
        self.sendMap = {}

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', self.port))
        # sock.bind(('192.168.21.37', self.port))
        sock.listen(5)

        print('服务端连接建立')
        while True:
            connection, address = sock.accept()
            print('客户端连接加入')
            try:
                print(address)
                print(sock.getpeername)
                username = "ID" + str(address[1])
                thread = websocket_thread(connection, username, self.clients, self.sendMap, self.port)
                thread.start()

            except socket.timeout:
                print('websocket connection timeout!')
        sock.close()
# if __name__ == '__main__':
    # server = websocket_server(9000)
    # server.start()


