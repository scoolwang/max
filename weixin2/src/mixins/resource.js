import {base64_encode} from './decode'
import {rootUrl} from './config'
// import * as config from './config.js'
import {getUserInfo} from './common.js'
function request (url, data, method="GET", unintercept) {
  let params = data || {}
  let userInfo = wx.getStorageSync('userInfo')
  let token1 = userInfo ? userInfo.token : ''
  // login()
  let pms = new Promise ((resolve, reject) => {
    if (userInfo && userInfo.token) {
      send (params, url, method="GET", unintercept).then((res)=> {
        resolve(res)
      })
    } else {
      login().then(res => {
        send(params, url, "GET", unintercept).then((res)=> {
          resolve(res)
        })
      })
      // login()
    }

  })
  return pms
}

function send (params, url, method="GET", unintercept) {
  let userinfo = wx.getStorageSync('userInfo')
  url = rootUrl + url
  console.log(base64_encode('client1:123456'))
  console.log('缓存的token', userinfo.token)
  return new Promise ((resolve, reject) =>{
    wx.cloud.callFunction({
      name: 'md52',
      data: {
        token: userinfo.token
      },
      complete: res => {
        console.log('callFunction test result: ', res)
        let token = res.result.token
        params.clientType = 'APP'
        params.deviceId = 'xiaochengxu'
        params.openId = res.result.openid
        console.log(url, '请求地址')
        // params.openId = res.result.openid
        wx.request({
          url: url,
          data: params,
          header: {
            client: base64_encode('client1:123456'),
            'access-token': token
          },
          method: method,
          success (p) {
            console.log(url, p, '请求成功')
            resolve(p.data)
          },
          fail (p) {
            console.log(url, '请求失败')
            reject(p)
          }
        })
      }
    })
  })

}

function login () {
  let pms = new Promise((resolve, reject) => {
    wx.cloud.callFunction({
      name: 'getUser',
      complete (res) {
        console.log('云函数getUser', res)
        loginValid(res).then((res) => {
          resolve(res)
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
  let loginPms = send({}, 'api/login', 'POST')

  return new Promise ((resolve, reject) => {
    loginPms.then((res) => {
      console.log(res, '登录')
      /** 登录成功 */
      if (res.code === '200') {
        /** 更新缓存信息 */
        // getUserInfo().then((userInfo) => {
        //   let info = Object.assign(userInfo, res.data)


        // })
        wx.setStorageSync('userInfo', res.data)
        resolve(res)
      }
       /** 登录用户未注册，进行注册 */
      if (res.code === '901') {
        getUserInfo().then((userInfo) => {
          send( {
            avatarUrl: userInfo.avatarUrl,
            name: userInfo.name,
            openId: openid
          }, 'api/register', 'POST').then((res)=> {
            console.log('注册', res)
            let info = Object.assign(userInfo, res.data)
            wx.setStorageSync('userInfo', info)
            resolve(res)
          })
        })
      }
    }, (err) => {
      console.log(err,'请求失败')
    })
  })
}
module.exports = {
  login,
  request
}
// export default request
