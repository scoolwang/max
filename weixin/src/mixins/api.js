import wepy from 'wepy'

function request (url, data, method="GET") {
  return new Promise ((resolve, reject) => {
    url = 'http://127.0.0.1:8000/' + url
    wepy.request({
      url: url,
      data: data,
      method: method,
      success (p) {
        resolve(p)
      },
      fail (p) {
        reject(p)
      }
    }, 'dfd')
  })
}
module.exports = {
  reg: (data) => {return request('api/register', data, 'POST')},
  login: (data) => {return request('api/login', data, 'POST')},
  getUser: (data) => {return request('api/getUser', data)},
  getActivityList: (data) => {return request('api/activityList', data)},
  addActivity: (data) => {return request('api/add/activity', data, 'POST')}
}

