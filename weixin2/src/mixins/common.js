// import wepy from 'wepy'
const qiniuUploader = require("./qiniuUploader")
/** 获取用户信息 */
function getUserInfo () {
  return new Promise((resolve, reject) => {
    let info = wx.getStorageSync('userInfo')
    if (!info) {
      wx.getUserInfo({
        success (res) {
          debugger
          console.log(res)
          info = res.userInfo
          wx.setStorageSync('userInfo', info)
          resolve(info)
        },
        fail (res) {
          console.log(res)
          reject(res)
        }
      })
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
  let nowDate = new Date().getTime() / 1000
  let spaceTime = nowDate - time / 1000
  let timeSpanStr = ''
  minute = minute < 10 ? '0' + minute : minute
  if (spaceTime <= 60) {
    timeSpanStr = '刚刚'
    if (spaceTime >=0) {
      timeSpanStr = parseInt(spaceTime) + '秒前'
    } else {
      if (year == now.getFullYear()) {
        timeSpanStr = month + '-' + day + ' ' + hour + ':' + minute;
      } else {
        timeSpanStr = year + '-' + month + '-' + day + ' ' + hour + ':' + minute
      }
    }
  } else if (60 * 1 < spaceTime && spaceTime <= 60 * 60) {
    timeSpanStr = Math.round((spaceTime / (60))) + '分钟前'
  } else if (60 * 60 * 1 < spaceTime && spaceTime <=  60 * 60 * 24) {
    timeSpanStr = Math.round(spaceTime / ( 60 * 60)) + '小时前';
  }
  else if (60 * 60 * 24 < spaceTime && spaceTime <=  60 * 60 * 24 * 15) {
    timeSpanStr = Math.round(spaceTime / ( 60 * 60 * 24)) + '天前';
  }
  else if (spaceTime > 60 * 60 * 24 * 15 && year == now.getFullYear()) {
    timeSpanStr = month + '-' + day + ' ' + hour + ':' + minute
  } else {
    timeSpanStr = year + '-' + month + '-' + day + ' ' + hour + ':' + minute
  }
  return timeSpanStr
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
  formatTime: formatCreateTime
}
