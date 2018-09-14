
function request (url, data, method="GET", unintercept) {
  let params = data || {}
  let userInfo = wx.getStorageSync('userInfo')
  params.token = userInfo ? userInfo.token : ''
  return new Promise ((resolve, reject) => {
    url = 'http://127.0.0.1:8000/' + url
    wx.request({
      url: url,
      data: params,
      method: method,
      success (p) {
        resolve(p.data)
      },
      fail (p) {
        reject(p)
      }
    })
  })
}
export default request
