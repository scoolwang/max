// 云函数入口文件
const cloud = require('wx-server-sdk')
const crypto = require("crypto")
cloud.init()
// 云函数入口函数
exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext()
  const time = new Date(new  Date().getTime()+28800000)
  var year = time.getFullYear()
  var month = time.getMonth() + 1
  var date = time.getDate()
  var hour = time.getHours()
  var mint = time.getMinutes()
  var key = 'guokaigewangtian'
  var iv = ''
  if (month < 10) {
    month = '0' + month
  }
  if (date < 10) {
    date = '0' + date
  }
  if (hour < 10) {
    hour = '0' + hour
  }
  if (mint < 10) {
    mint = '0' + mint
  }
  // iv = year + '-' + month + '-' + date + '-' + hour + ':' + hour
  iv = 'abcdefg123456789'
  // var key = new Buffer(se, 'base64').toString('hex')
  console.log('便宜量', event.token)
  var data = wxContext.OPENID + event.token
  console.log(data, '加密字符串')
  // var data = '123456'
  var client = 'wxe37b540617a53b3a:' + '30bb58edaaa9f9ab979c8e7d121d4bbe'
  var cipher = crypto.createCipheriv('aes-128-cbc', key, iv)
  cipher.setAutoPadding(true)
  var crypted = cipher.update(data, 'utf8', 'hex')
  var up = crypted
  // var tt = cipher.final('hex')
  console.log('final')
  crypted += cipher.final('hex')

  var md5 = crypto.createHash('md5')

  var ss = md5.update('openid' + iv + key)
  var sign = ss.digest('hex')
  console.log('token', crypted)
  console.log('clientStr', crypted)
  // crypted = new Buffer(crypted, 'hex').toString('base64');
  return {
    data: data,
    key: key,
    iv: iv,
    token: crypted,
    sign: sign,
    // clientStr: clientStr,
    openid: wxContext.OPENID
  }
}
