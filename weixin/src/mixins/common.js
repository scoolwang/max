import wepy from 'wepy'
/** 获取用户信息 */
function getUserInfo () {
  return new Promise((resolve, reject) => {
    let info = wepy.getStorageSync('userInfo')
    if (!info) {
      wepy.getUserInfo({
        success (res) {
          debugger
          console.log(res)
          info = res.userInfo
          wepy.setStorageSync('userInfo', info)
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
