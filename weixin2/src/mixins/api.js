import request from './resource'
module.exports = {
  reg: (data) => {return request('api/register', data, 'POST')},
  login: (data) => {return request('api/login', data, 'POST')},
  getUser: (data) => {return request('api/getUser', data)},
  getActivityList: (data) => {return request('api/activityList', data)},
  addActivity: (data) => {return request('api/add/activity', data, 'POST')}
}

