import request from './resource'
module.exports = {
  reg: (data) => {return request('api/register', data, 'POST')},
  login: (data) => {return request('api/login', data, 'POST')},
  getUser: (data) => {return request('api/getUser', data)},
  // 活动列表
  getActivityList: (data) => {return request('demo/activity/findActivityBy', data, 'POST')},
  /** 活动更新 */
  updateActivity: (data) => {return request('demo/activity/update', data)},
  /** 活动删除 */
  delActivity: (data) => {return request('demo/activity/del', data)},
  /** 发布活动 */
  addActivity: (data) => {return request('demo/activity/save', data, 'POST')},
  getUserById: (data) => {return request('api/userinfo/id', data)},
  getMsg: (data) => {return request('api/getMsg', data)},
  addMsg: (data) => {return request('api/add/msg', data, 'POST')},
  /** 大神认证 */
  addAuth: (data) => {return request('api/auth', data, 'POST')},
  /** 加入活动呢 */
  joinActivity: (data) => {return request('api/join/activity', data, 'POST')},
  /** 注册 */
  reg2: (data) => {return request('server/app/reg/register', data, 'POST')},
  /** 获取用户信息 */
  getUser2: (data) => {return request('server/app/user/detail', data, 'POST')},
  /** 获取用户token */
  getToken: (data) => {return request('server/authentication/app', data, 'POST')},
  /** 获取未读消息 */
  getUnreadMsg: (data) => {return request('demo/msg/findUnReadMsg', data, 'POST')},
  /** 读消息 */
  readMsg: (data) => {return request('demo/msg/setMsgReaded', data, 'POST')},
  /** 添加系统消息 */
  addMsg: (data) => {return request('demo/msg/addSysMsg', data, 'POST')},
  /** 七牛token */
  qiniuToken: (data) => {return request('demo/qn/uploadToken', data, 'POST')}
}

