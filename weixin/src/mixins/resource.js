import wepy from 'wepy'
function config (p) {
  debugger
  if (p._unintercept) {
    delete p._unintercept
    return p
  }
  let userInfo = wepy.getStorageSync('userInfo')
  p.data = p.data ? p.data : {}
  p.data.token = userInfo ? userInfo.token : ''
  p.data.time = 1213
  return p
}
function success (p) {
  return p.data
}
function fail (p) {
  return p
}
function complete (p) {
  return p
}
module.exports = {
  config,
  success,
  fail,
  complete
}
