// import wepy from 'wepy'
import * as config from './config.js'
import * as api from './api.js'
import {getUserInfo} from './common.js'
function login () {
  let pms = new Promise((resolve, reject) => {
    wx.cloud.callFunction({
      name: 'getUser',
      complete (res) {
        console.log('云函数getUser', res)
        loginValid(res).then(() => {
          resolve()
        })
      }
    })
  })
  return pms
}

function loginValid (res) {
  // let openid = res.openid
  let openid = 'abcdef'
  wx.setStorageSync('openid', res.openid)
  /** 打开小程序，系统登录 */
  let pms = api.login()

  pms.then((res) => {
    console.log(res)
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
          console.log('用户信息', userInfo)
          api.reg({
            name: userInfo.name,
            avatarUrl: userInfo.avatarUrl,
            openId: openid
          }).then((res) => {
            /** 注册成功更新用户信息 */
            let info = Object.assign(userInfo, res.data)
            wx.setStorageSync('userInfo', info)
          })
        })
      }
  })
  return pms
}

module.exports = {
  login
}
