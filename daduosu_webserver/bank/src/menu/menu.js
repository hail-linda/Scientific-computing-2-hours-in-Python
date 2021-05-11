let menu = {};

/* https://fontawesome.dashgame.com/ */
/*
首页
 @type {{name: string, path: string, icon: string}}
 */
menu.home = {
  name: '首页',
  path: '/',
  icon: 'fa fa-tachometer',
}

/*
Console
@type {{name: string, icon: string, children: {}}}
*/
menu.console = {
  name: '控制台',
  icon: 'fa fa-terminal',
  children: {}
}
let console = menu.console.children;
// charts.line = {
//   name: '折线图',
//   path: '/charts_line'
// };
// charts.bar = {
//   name: '柱状图',
//   path: '/charts_bar'
// }

/*
map
@type {{name: string, icon: string, children: {}}}
*/
menu.order = {
  name: '订单管理',
  icon: 'fa fa-shopping-bag',
  children: {}
}
let order = menu.order.children;
// map.baidu = {
//   name: '百度地图',
//   path: '/map_baidu'
// };

/*
提现记录
@type {{name: string, icon: string, children: {}}}
*/
menu.withdraw = {
  name: '提现记录',
  icon: 'fa fa-money',
  children: {}
};
let withdraw = menu.withdraw.children;
withdraw.font_awesome = {
  name: 'T+0提现记录',
  path: '/font_awesome'
};
withdraw.element_icon = {
  name: '提现历史记录',
  path: '/element_icon',
}

/*
资金报表
@type {{name: string, icon: string, children: {}}}
*/
menu.fund = {
  name: '资金报表',
  icon: 'fa fa-signal',
  children: {}
}
let fund = menu.fund.children;
fund.cashFlow = {
  name: '资金流水',
  path: '/cash_flow',
}
fund.channelFlow = {
  name: '通道流水',
  path: '/channel_flow',
}
/*
会员管理
@type {{name: string, icon: string, children: {}}}
*/
menu.member = {
  name: '会员管理',
  icon: 'fa fa-user-plus',
  children: {}
}
/*
通道管理
@type {{name: string, icon: string, children: {}}}
*/
menu.pass = {
  name: '通道管理',
  icon: 'fa fa-retweet',
  children: {}
}

/*
帐号管理
@type {{name: string, icon: string, children: {}}}
*/
menu.account = {
  name: '帐号管理',
  icon: 'fa fa-bank',
  children: {}
}

/*
系统设置
@type {{name: string, icon: string, children: {}}}
*/
menu.sys = {
  name: '系统设置',
  icon: 'fa fa-wrench',
  children: {}
}
/**
 * 用户管理
 * @type {{name: string, icon: string, children: {}}}

menu.user_manage = {
  name: '用户管理',
  icon: 'fa fa-user-circle-o',
  children: {}
};
let UserManage = menu.user_manage.children;
UserManage.user = {
  name: '用户列表',
  path: '/user_manage',
};
 */
export default menu;
