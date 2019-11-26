from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import random, string
import datetime

class EncryptAES():
  def __init__(self):
    self.key = 'guokaigewangtian'.encode('utf-8')
    # self.iv = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M')
    self.iv = 'abcdefg123456789'.encode('utf-8')
    self.mode = AES.MODE_CBC

  # 加密
  # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）
  def encrypt(self, text):
    cryptor = AES.new(self.key, self.mode, self.iv )
    #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
    #length = 16
    text=self.bytePad(text,16)
    #add = length - (count % length)
    #text = text + ('\0' * add)
    text = text.encode('utf-8')
    self.ciphertext = cryptor.encrypt(text)
    #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    #所以这里统一把加密后的字符串转化为16进制字符串
    # return self.ciphertext
    return b2a_hex(self.ciphertext).decode()

  #解密后，去掉补足的空格用strip() 去掉
  def decrypt(self, text):
      cryptor = AES.new(self.key, self.mode, self.iv )
      plain_text = cryptor.decrypt(a2b_hex(text))
      # plain_text = cryptor.decrypt(text)
      #printMemLog2(plain_text)
      #print plain_text
      # print(plain_text,  '揭秘')
      # print(self.byteUnpad(plain_text),  '揭秘')
      return self.byteUnpad(plain_text.decode())

  @staticmethod
  def get_random_string(length=8):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))

  @staticmethod
  def bytePad(text,byteAlignLen=16):
      count=len(text)
      mod_num=count%byteAlignLen
      if  mod_num==0:
          return text
      add_num=byteAlignLen-mod_num
      # print("bytePad:" ,add_num)
      return text+chr(add_num)*add_num

  @staticmethod
  def byteUnpad(text,byteAlignLen=16):
      count=len(text)
      # print("byteUnpad:",text)
      mod_num=count%byteAlignLen
      # print("byteUnpad:",mod_num)
      assert mod_num==0
      lastChar=text[-1]
      # print(lastChar, '上一个')
      lastLen=ord(lastChar)
      # print(lastLen, '上一个2')
      lastChunk=text[-lastLen:]
      # print(lastChunk, '上一个3')
      if lastChunk==chr(lastLen)*lastLen:
          # print(chr(lastLen), chr(lastLen)*lastLen, 'chr(lastLen)')
          # print(lastLen, 'lastLen')
          # print(text[:-lastLen])
          #print "byteUnpad"
          return text[:-lastLen]
      return text

if __name__ == '__main__':
    aes = EncryptAES()  # 初始化密钥
    e_result = aes.encrypt("123456")
    print(e_result)
    print(aes.decrypt(e_result))
    d_result = aes.decrypt("fe0269caf1dad12cb384218c8326ab8afcf3d36db4e72b873e075472c258543a810055977150b3d330de916a536f113113fe5386af7f6e9e23d4bb222aa1e9aa")
    # d_result = aes.decrypt(e_result)

    print(d_result)
