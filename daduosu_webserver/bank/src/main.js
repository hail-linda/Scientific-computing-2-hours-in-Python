// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import axios from 'axios'
import qs from 'qs'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import request from './utils/request'
import Mock from './mock'
Mock.bootstrap();
//加载全局样式
import "@/styles/index.scss"
// css
import './assets/css/style.css'
Vue.use(ElementUI)
Vue.prototype.$qs = qs;
Vue.config.productionTip = false
router.beforeEach((to, from, next) => {
  if (to.path == '/login') {
    sessionStorage.removeItem('user');
  }
  let user = JSON.parse(sessionStorage.getItem('user'));
  if (!user && to.path != '/login') {
    next({
      path: '/login'
    })
  } else {
    next()
  }
})
axios.get('./static/config.json').then(response=> {
  let data = response.data||{};
  Vue.prototype.$API_CONFIG = data;
  request.defaults.baseURL = data.BASE_API||"";
})
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>'
})

