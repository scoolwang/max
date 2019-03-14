import {base64_encode} from './decode'
import {rootUrl} from './config'
function request (url, data, method="GET", unintercept) {
  let params = data || {}
  let userInfo = wx.getStorageSync('userInfo')
  let token1 = userInfo ? userInfo.token : ''
  return new Promise ((resolve, reject) => {
    url = rootUrl + url
    console.log(base64_encode('client1:123456'))
    wx.cloud.callFunction({
      name: 'md5',
      data: {
        str: 'test12321郭凯歌'
      },
      complete: res => {
        console.log('callFunction test result: ', res)
        let token = res.result.token
        params.clientType = 'APP'
        params.deviceId = 'xiaochengxu'
        params.openId = token
        // params.openId = res.result.openid
        wx.request({
          url: url,
          data: params,
          header: {
            client: base64_encode('client1:123456'),
            access_token: token
          },
          method: method,
          success (p) {
            resolve(p.data)
          },
          fail (p) {
            reject(p)
          }
        })
      }
    })


  })
}
export default request
