import {request} from './resource'
module.exports = {
  reg: (data) => {return request('api/register', data, 'POST')},
  login: (data) => {return request('api/login', data, 'POST')},
  getUser: (data) => {return request('api/getUser', data)},
  getActivityList: (data) => {return request('api/activityList', data)},
  /** 发布活动 */
  addActivity: (data) => {return request('api/add/activity', data, 'POST')},
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
  // getUnreadMsg: (data) => {return request('demo/msg/findUnReadMsg', data, 'POST')},
  getUnreadMsg: (data) => {return request('api/unread/msg', data, 'POST')},
  /** 读消息 */
  readMsg: (data) => {return request('demo/msg/setMsgReaded', data, 'POST')},
  /** 获取系统消息 */
  getSysMsg: (data) => {return request('api/sys/msg', data)},
  getChatUnreadMsg: (data) => {return request('api/unread/chat/msg', data)},
  /** 获取活动详情 */
  getActivity: (data) => {return request('api/get/activity', data)},
  /** 获取活动申请列表 */
  getActivityUsers: (data) => {return request('api/get/activity/users', data)},
  /** 修改乘客状态 */
  editStatus: (data) => {return request('api/get/activity/status', data)},
  addComment: (data) => {return request('api/add/comment', data, 'POST')},
  getMsgToken: (data) => {return request('api/upload/token', data)},
  getComment: (data) => {return request('api/get/comment', data)},
  getReply: (data) => {return request('api/get/reply', data)}
}

