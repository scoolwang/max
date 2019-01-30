import request from './resource'
module.exports = {
  reg: (data) => {return request('api/register', data, 'POST')},
  login: (data) => {return request('api/login', data, 'POST')},
  getUser: (data) => {return request('api/getUser', data)},
  getActivityList: (data) => {return request('api/activityList', data)},
  addActivity: (data) => {return request('api/add/activity', data, 'POST')},
  getUserById: (data) => {return request('api/userinfo/id', data)},
  getUnreadMsg: (data) => {return request('api/unread/msg', data)},
  getMsg: (data) => {return request('api/getMsg', data)},
  addMsg: (data) => {return request('api/add/msg', data), 'POST'}
}

