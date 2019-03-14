// import wepy from 'wepy'
import * as config from './config.js'
import * as api from './api.js'
import {getUserInfo} from './common.js'
function login () {
  wx.cloud.callFunction({
    name: 'getUser',
    complete (res) {
      loginValid(res)
    }
  })
}

function loginValid (res) {
  // let openid = res.openid
  let openid = 'abcdef'
  wx.setStorageSync('openid', res.openid)
  /** 打开小程序，系统登录 */
  let pms = api.getToken()

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
