import {request} from './resource'
module.exports = {
  reg: (data) => {return request('api/register', data, 'POST')},
  login: (data) => {return request('api/login', data, 'POST')},
  getUser: (data) => {return request('api/get/user', data)},
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
  /** 获取用户的未读消息并修改消息状态 */
  getUnreadMsg: (data) => {return request('api/unread/msg', data, 'POST')},
  /** 读消息 */
  // readMsg: (data) => {return request('demo/msg/setMsgReaded', data, 'POST')},
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
  getReply: (data) => {return request('api/get/reply', data)},
  getAuth: (data) => {return request('api/get/auth', data)},
  updateUser: (data) => {return request('api/user/update', data)},
  getUserAuth: (data) => {return request('api/user/auth', data)},
  getJoin: (data) => {return request('api/get/join', data)},
  recallJoin: (data) => {return request('api/recall/join', data)},
  getGameInfo: (data) => {return request('api/game/info', data)},
  careUser: (data) => {return request('api/care/user', data)},
  /** 评价用户 */
  addWords: (data) => {return request('api/add/words', data)},
  getWords: (data) => {return request('api/get/words', data)},
  /** 获取用户已认证的游戏信息 */
  getUserAuthGame: (data) => {return request('api/user/auth/game', data)},
  /** 标记消息为已读 */
  readMsg: (data) => {return request('api/read/msg', data)},
  getGameList: (data) => {return request('api/get/gamelist', data)},
  getFans: (data) => {return request('api/get/fans', data)},
  getCare: (data) => {return request('api/get/care', data)},
  getUnreadMsgTotal: (data) => {return request('api/unread/msg/total', data)},
  /** 读消息通过id */
  readMsgById: (data) => {return request('api/read/msg/id', data)}

}

