// import wepy from 'wepy'
import * as config from './config.js'
import * as api from './api.js'
import {getUserInfo} from './common.js'
function login () {
  wx.login({
    success (res) {
      const code = res.code
      wx.request({
        url: 'https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code',
        _unintercept: true,
        data: {
          appid: config.appid,
          secret: config.secret,
          js_code: code,
          grant_type: 'authorization_code'
        },
        success (res) {
          loginValid(res)
        },
        complete (res) {
        }
      })
    }
  })
}

function loginValid (res) {
  // let openid = res.openid
  let openid = 'abcdef'
  wx.setStorageSync('openid', res.openid)
  /** 打开小程序，系统登录 */
  let pms = api.login({
    // openId: res.openid
    openId: openid
  })

  pms.then((res) => {
      /** 登录成功 */
      if (res.code === '200') {
        /** 更新缓存信息 */
        getUserInfo().then((userInfo) => {
          let info = Object.assign(userInfo, res.data)
          wx.setStorageSync('userInfo', info)
        })
      }
       /** 登录用户未注册，进行注册 */
      if (res.code === '901') {
        getUserInfo().then((userInfo) => {
          api.reg({
            name: userInfo.nickName,
            openId: openid
          }).then((res) => {
            /** 注册成功更新用户信息 */
            let info = Object.assign(userInfo, res.data)
            wx.setStorageSync('userInfo', info)
          })
        })
      }
  })
}

module.exports = {
  login
}
