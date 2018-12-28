#-*- coding:utf8 -*-

import threading
import hashlib
import socket
import base64
import struct
import json
import time
from wx import models
global clients
clients = {}
sendMap = {}
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
    server = websocket_server(9000)
    server.start()

#客户端处理线程
class websocket_thread(threading.Thread):
    def __init__(self, connection, username):
        super(websocket_thread, self).__init__()
        print(connection.getpeername())
        self.connection = connection
        self.username = username

    def run(self):
        print('new websocket client joined!')
        data = self.connection.recv(2048)
        headers = self.parse_headers(data)
        token = self.generate_token(headers['Sec-WebSocket-Key'])
        print('headers数据')
        print(data)
        str2 = 'HTTP/1.1 101 Switching Protocols \r\n' \
                'Upgrade: WebSocket\r\n'\
                'Connection: Upgrade\r\n'\
                'Sec-WebSocket-Accept: %s\r\n\r\n' % token
        str2 = str2.encode('utf8')
        sendMap['id'+ headers['data']['from']] = self.username
        print(sendMap)
        self.connection.send(str2)
        while True:
            print('接受数据')
            try:
                print('接受数据1')
                data = self.connection.recv(2048)
                print(data)
            except Exception as e:
                print('接受数据3')
                print("unexpected error: ", e)
                clients.pop(self.username)
                break
            print('接受数据3')
            if not data:
                return
            print('data数据')
            print(data)
            data = self.parse_data(data)
            # if len(data) == 0:
            #     continue
            message = data
            print('发送的数据')
            print(message)
            print(time.time() * 1000)
            sqlData = {
                'msg': message,
                'sendId': headers['data']['from'],
                'receiveId': headers['data']['to'],
                'type': 0,
                'time': time.time() * 1000
            }
            msgData = {
                'data': message,
                'from': headers['data']['from'],
                'to': headers['data']['to'],
                'type': '0',
                'time': time.time() * 1000
            }
            toid = 'id' + headers['data']['to']
            fromid = 'id' + headers['data']['from']
            print('clients')
            print(clients)
            print('sendMap')
            print(sendMap)
            toSocketId = sendMap.get(toid)
            print(toid)
            print(toSocketId)
            if not toSocketId or not data:
                if not toSocketId:
                    # toSocketId = sendMap.get(fromid)
                    models.addMsg(sqlData)
            else:
                message = json.dumps(msgData)
                notify(message, clients[toSocketId])

    def parse_data(self, info):
        code_len = info[1] & 0x7f
        if code_len == 0x7e:
            extend_payload_len = info[2:4]
            mask = info[4:8]
            decoded = info[8:]
        elif code_len == 0x7f:
            extend_payload_len = info[2:10]
            mask = info[10:14]
            decoded = info[14:]
        else:
            extend_payload_len = None
            mask = info[2:6]
            decoded = info[6:]
        bytes_list = bytearray()
        for i in range(len(decoded)):
            chunk = decoded[i] ^ mask[i % 4]
            bytes_list.append(chunk)
        raw_str = str(bytes_list, encoding="utf-8")
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
        print('key等他的')
        # print(key.encode('utf8'))
        # key = str(key)
        print(key)
        ser_key = hashlib.sha1(key).digest()
        # ser_key = str(ser_key)
        print('加密后')
        ser_key = base64.b64encode(ser_key)
        ser_key = ser_key.decode('utf8')
        print(ser_key)
        return ser_key

#服务端
class websocket_server(threading.Thread):
    def __init__(self, port):
        super(websocket_server, self).__init__()
        self.port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('192.168.21.37', self.port))
        sock.listen(5)

        print('websocket server started!')
        while True:
            connection, address = sock.accept()
            try:
                print(address)
                print(sock.getpeername)
                username = "ID" + str(address[1])
                thread = websocket_thread(connection, username)
                thread.start()
                clients[username] = connection
            except socket.timeout:
                print('websocket connection timeout!')

if __name__ == '__main__':
    server = websocket_server(9000)
    server.start()


