// import wepy from 'wepy'
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
module.exports = {
  getUserInfo
}
