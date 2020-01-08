// import wepy from 'wepy'
import {formateTime} from 'common.js'
const qiniuUploader = require("./qiniuUploader")
let fileSystemManager = wx.getFileSystemManager()
// import {getUser} from 'api.js'
/** 获取用户信息 */
function getUserInfo () {
  return new Promise((resolve, reject) => {
    let info = wx.getStorageSync('userInfo')
    if (!info) {
      resolve(info)
    } else {
      resolve(info)
    }
  })

}
function base64_encode (str) { // 编码，配合encodeURIComponent使用
    var c1, c2, c3;
    var base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    var i = 0, len = str.length, strin = '';
    while (i < len) {
        c1 = str.charCodeAt(i++) & 0xff;
        if (i == len) {
            strin += base64EncodeChars.charAt(c1 >> 2);
            strin += base64EncodeChars.charAt((c1 & 0x3) << 4);
            strin += "==";
            break;
        }
        c2 = str.charCodeAt(i++);
        if (i == len) {
            strin += base64EncodeChars.charAt(c1 >> 2);
            strin += base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
            strin += base64EncodeChars.charAt((c2 & 0xF) << 2);
            strin += "=";
            break;
        }
        c3 = str.charCodeAt(i++);
        strin += base64EncodeChars.charAt(c1 >> 2);
        strin += base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
        strin += base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6));
        strin += base64EncodeChars.charAt(c3 & 0x3F)
    }
    return strin
}
function uploadImg (filePath, key) {
  let pms = new Promise((resolve, reject) => {
    qiniuUploader.upload(filePath, (res) => {
      resolve({
        imageUrl: res
      })
      console.log(res)
    }, (error) => {
      reject(error)
      console.log(error)
    })
  })
  return pms
}
function formatTime (time) {
  let dateTime = new Date(time)
  let year = dateTime.getFullYear()
  let month = dateTime.getMonth() + 1
  let day = dateTime.getDate()
  let hour = dateTime.getHours()
  let minute = dateTime.getMinutes()
  let second = dateTime.getSeconds()
  let nowDate = new Date().getTime()
  let str = hour + ':' + (minute < 10 ? '0' + minute : minute)
  if (nowDate - time <= 60 * 60 * 12) {
    return str
  } else {
    return year + '-' + month + '-' + day + ' ' + str
  }
}
function formatCreateTime (time) {
  let dateTime = new Date(time)
  let year = dateTime.getFullYear()
  let month = dateTime.getMonth() + 1
  let day = dateTime.getDate()
  let hour = dateTime.getHours()
  let minute = dateTime.getMinutes()
  let second = dateTime.getSeconds()
  let now = new Date()
  let nowDate = (new Date().getTime()) / 1000
  let spaceTime = nowDate - time / 1000
  let timeSpanStr = ''
  let isTody = false
  minute = minute < 10 ? '0' + minute : minute
  if (spaceTime <= 60) {
    timeSpanStr = '刚刚'

    if (spaceTime >=0) {
      isTody = true
      timeSpanStr = parseInt(spaceTime) + '秒前'
    } else {
      if (year == now.getFullYear()) {
        timeSpanStr = month + '-' + day + ' ' + hour + ':' + minute;
      } else {
        timeSpanStr = year + '-' + month + '-' + day + ' ' + hour + ':' + minute
      }
      isTody = false
    }
  } else if (60 * 1 < spaceTime && spaceTime <= 60 * 60) {
    isTody = true
    timeSpanStr = Math.round((spaceTime / (60))) + '分钟前'
  } else if (60 * 60 * 1 < spaceTime && spaceTime <=  60 * 60 * 24) {
    isTody = true
    timeSpanStr = Math.round(spaceTime / ( 60 * 60)) + '小时前';
  }
  else if (60 * 60 * 24 < spaceTime && spaceTime <=  60 * 60 * 24 * 15) {
    isTody = false
    timeSpanStr = Math.round(spaceTime / ( 60 * 60 * 24)) + '天前';
  }
  else if (spaceTime > 60 * 60 * 24 * 15 && year == now.getFullYear()) {
    isTody = false
    timeSpanStr = month + '-' + day + ' ' + hour + ':' + minute
  } else {
    isTody = false
    timeSpanStr = year + '-' + month + '-' + day + ' ' + hour + ':' + minute
  }
  return {
    str: timeSpanStr,
    isTody: isTody,
    spaceTime: spaceTime,
    y: year,
    m: month,
    d: day,
    h: hour,
    mt: minute
  }
}

function formatStartTime (time) {
  let dateTime = new Date(time)
  let year = dateTime.getFullYear()
  let month = dateTime.getMonth() + 1
  let day = dateTime.getDate()
  let hour = dateTime.getHours()
  let minute = dateTime.getMinutes()
  let second = dateTime.getSeconds()
  let tody = new Date() // 今天
  let todyY = tody.getFullYear()
  let todyM = tody.getMonth() + 1
  let todyD = tody.getDate()
  let tommory = new Date(tody.getTime() + (24 * 60 * 60 * 1000)) // 明天
  let tommoryY = tommory.getFullYear()
  let tommoryM = tommory.getMonth() + 1
  let tommoryD = tommory.getDate()
  let tommory1 = new Date(tody.getTime() + (24 * 60 * 60 * 1000 * 2)) // 后天
  let tommory1Y = tommory1.getFullYear()
  let tommory1M = tommory1.getMonth() + 1
  let tommory1D = tommory1.getDate()
  let am = ''
  let d = ''
  let timeStr = ''
  if (hour >= 12 && hour < 18) {
    am = '下午'
  } else if (hour >= 18 && hour < 24) {
    am = '晚上'
  } else {
    am = '上午'
  }
  if (year === todyY && month === todyM && day === todyD) {
    d = '今天'
  }
  if (year === tommoryY && month === tommoryM && day === tommoryD) {
    d = '明天'
  }
  if (year === tommory1Y && month === tommory1M && day === tommory1D) {
    d = '后天'
  }
  minute = minute < 10 ? ('0' + minute ): minute
  if (d) {
    timeStr = d  + ' ' + hour + ':' + minute
  } else {
    timeStr = year + '-' + month + '-' + day + ' ' + hour + ':' + minute
  }
  return timeStr
}
/** data
 *  data.time 时间戳
 *  data.from 聊天对象用户id
 *  data.data 聊天消息
 *  data.type 消息类型 0：用户聊天 1：时间戳
 *  data.avatarUrl 消息主体头像
 *  data.nick 消息主体昵称
 *  data.toAvatarUrl 消息接受者头像
 *  data.toNick 消息接受者昵称
 *  lastTimeTag 最后一条消息的时间点
 */

function msgHandle (data, lastTimeTag, fileDir) {
  let time = data.time
  let innserTag = false
  let arry = []
  let timeTag = formateMsgTime(time)
  if (!lastTimeTag) {
    innserTag = true
  } else {
    if (time - lastTimeTag > 5 * 60 * 1000) {
      innserTag = true
    }
  }
  if (innserTag) {
    let obj = {
      type: 0,
      time: time,
      timeStr: timeTag[0] + '年' + timeTag[1] + '月' + timeTag[2] + '日 ' + (timeTag[3] < 10 ? '0' + timeTag[3] : timeTag[3]) + ':' + (timeTag[4] < 10 ? '0' + timeTag[4] : timeTag[4]),
      data: timeTag[3] + ':' + timeTag[4]
    }
    arry.push(obj)
    lastTimeTag = time
    writeChatFile(obj, fileDir)
  }
  arry.push(data)
  writeChatFile(data, fileDir)
  return {
    data: arry,
    lastTimeTag: time
  }
}
function formateMsgTime (time) {
  let d = time ? new Date(time) : new Date()
  let y = d.getFullYear()
  let m = d.getMonth() - 1
  let day = d.getDay()
  let hh = d.getHours()
  let mm = d.getMinutes()
  let ss = d.getSeconds()

  return [y, m, day, hh, mm, ss]
}
// 把聊天记录写入到本地文件
function writeChatFile (str, fileDir) {
  let data = JSON.stringify(str) + '\r\n\r\n'
  // let fileDir = wx.env.USER_DATA_PATH +  '/test.txt'
  console.log('文件目录')
  fileSystemManager.stat({
    path: fileDir,
    success: res => {
      console.log('文件存在', res)
      fileSystemManager.appendFile({
        // filePath: res.savedFilePath,
        filePath: fileDir,
        data: data,
        encoding: 'utf8',
        success (res) {
          console.log('追加1', res)
        },
        fail (res) {
          console.log('追加2', res)
        }
      })
    },
    fail: res => {
      console.log('文件不存在', fileDir, res)
      /*
       * writeFile第一天消息无法写入，所以先新建文件，再appFile追加新消息
       *
       *
       */
      fileSystemManager.writeFile({
        // filePath: res.savedFilePath,
        filePath: fileDir,
        data: '\r\n\r\n',
        encoding: 'utf8',
        success (res) {
          fileSystemManager.appendFile({
            // filePath: res.savedFilePath,
            filePath: fileDir,
            data: data,
            encoding: 'utf8',
            success (res) {
              console.log('追加3', res)
            },
            fail (res) {
              console.log('追加4', res)
            }
          })
        },
        fail (res) {
          console.log('写入失败', res)
        }
      })
    }
  })
}
qiniuUploader.init({
  region: 'ECN',
  uploadURL: 'http://upload.qiniup.com',
  domain: 'http://pp.vlgcty.com',
  uptokenURL: 'http://192.168.21.37:8000/api/upload/token'
})
// qiniuUploader.init({
//   region: 'ECN',
//   scope: 'yuexing',
//   key: 'chat_photo_9894d66cb7a84a369a2a466f21f05de6.jpg',
//   uploadURL: 'http://upload.qiniup.com',
//   domain: 'http://xinrongmuye.cn',
//   uptoken: 'FAdGTN448EvmDPYBwaU6fIFXPClILA_onjkfNtJ4:5J7hfH_UC4KrdXXzi3Trcz9MdOY=:eyJlbmRVc2VyIjoieXVlIiwic2NvcGUiOiJ5dWV4aW5nOmNoYXRfcGhvdG9fOTg5NGQ2NmNiN2E4NGEzNjlhMmE0NjZmMjFmMDVkZTYuanBnIiwiZGVhZGxpbmUiOjUxNzQzODExNDMzMX0='
// })
module.exports = {
  getUserInfo,
  base64_encode,
  uploadImg,
  msgHandle,
  formatStartTime,
  formatTime: formatCreateTime
}
