import Vue from 'vue'
import Router from 'vue-router'
import request from "../utils/request";
Vue.use(Router)
export default new Router({
  routes: [{
    path: '/login',
    component: resolve => require(['@/views/login/index.vue'], resolve),
  },
    {
      path: '/',
      component: resolve => require(['@/views/layout/main.vue'], resolve),
      meta: {
        title: '首页',
        keepAlive: false, // 不需要缓存
      },
      children: [{
        path: '/',
        name: 'Dashboard',
        meta: {
          title: '首页',
          keepAlive: true // 需要被缓存
        },
        component: resolve => require(['@/views/home/index.vue'], resolve),
      },
        {
          path:'/cash_flow',
          name:'CashFlow',
          meta:{
            title:'资金流水',
            keepAlive: false
          },
          component:resolve=>require(['@/views/fund/cashFlow.vue'],resolve)
        }
        // {
        //   path: '/charts_line',
        //   name: 'Line',
        //   meta: {
        //     title: '折线图',
        //     keepAlive: false
        //   },
        //   component: resolve => require(['@/views/charts/Line.vue'], resolve),
        // },
        // {
        //   path: '/charts_bar',
        //   name: 'Bar',
        //   meta: {
        //     title: '柱状图',
        //     keepAlive: false
        //   },
        //   component: resolve => require(['@/views/charts/Bar.vue'], resolve),
        // },
        // {
        //   path: '/font_awesome',
        //   name: 'FontAwesome',
        //   meta: {
        //     title: 'FontAwesome 图标',
        //     keepAlive: false
        //   },
        //   component: resolve => require(['@/views/icon/FontAwesome.vue'], resolve),
        // },
        // {
        //   path: '/element_icon',
        //   name: 'ElementIcon',
        //   meta: {
        //     title: 'Element 图标',
        //     keepAlive: false
        //   },
        //   component: resolve => require(['@/views/icon/ElementIcon.vue'], resolve),
        // },
        // {
        //   path: '/map_baidu',
        //   name: 'Baidu',
        //   meta: {
        //     title: '百度地图',
        //     keepAlive: false
        //   },
        //   component: resolve => require(['@/views/map/Baidu.vue'], resolve),
        // },
        // {
        //   path: '/table_manage',
        //   name: 'Table',
        //   meta: {
        //     title: '表格',
        //     keepAlive: false
        //   },
        //   component: resolve => require(['@/views/tableManage/index.vue'], resolve),
        // },
        /*
                {
                  path: '/user_manage',
                  name: 'UserManage',
                  meta: {
                    title: '用户列表',
                    keepAlive: true
                  },
                  component: resolve => require(['@/views/userManage/index.vue'], resolve),
                },
                 */

      ]
    }
  ]
})
