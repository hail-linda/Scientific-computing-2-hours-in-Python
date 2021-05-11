<!--  -->
<template>
  <div class='main'>
    <!-- B 顶部菜单 -->
    <div class="header">
      <div class="logo">
        <span class="big">taotao商城代理平台</span>
        <span class="min">
          <img src="../../assets/images/logo.svg">
        </span>
      </div>

      <div class="header-right">
        <span class="header-btn"
              @click="screenfullToggle"
              title="全屏">
          <i class="fa fa-arrows-alt"></i>
        </span>

        <el-dropdown trigger="click">
          <span class="header-btn">
            <i class="el-icon-setting"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <div class="setting-category">
              <el-switch v-model="switchTabBar"
                         @click="saveSwitchTabBar"
                         active-text="开启TabBar"
                         inactive-text="关闭TabBar">
              </el-switch>
              <el-switch v-model="fixedTabBar"
                         v-if="switchTabBar"
                         class="fixedTabBar"
                         @click="saveFixedTabBar"
                         active-text="固定在顶部"
                         inactive-text="随页面滚动">
              </el-switch>
            </div>
          </el-dropdown-menu>
        </el-dropdown>

        <span class="header-btn">
          <el-badge :value="3">
            <i class="el-icon-bell"></i>
          </el-badge>
        </span>

        <el-dropdown>
          <span class="header-btn">
            {{sysUserName}}
            <i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
						<a target='_blank' href="https://gitee.com/zpt360/element-admin.git">
						  <el-dropdown-item><i class="fa fa-cog"></i>码云地址</el-dropdown-item>
						</a>
            <el-dropdown-item @click.native="logout"><i class="fa fa-key"></i> 退出系统</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>

      </div>
    </div>
    <!-- E 顶部菜单 -->

    <div class="app">
      <div class="aside">
        <div class="menu">
          <el-menu router
                   class="el-menu-vertical-demo"
                   background-color="#222d32"
                   text-color="#fff"
                   :default-active="$route.path">
            <template v-for="(menu_v,menu_k) in menu">
              <el-submenu v-if="menu_v.children"
                          :index="menu_k">
                <template slot="title">
                  <i :class="menu_v.icon"></i>
                  <span>{{menu_v.name}}</span>
                </template>

                <el-menu-item v-for="(menuChildren_v,menuChildren_k) in menu_v.children"
                              :key="menuChildren_k"
                              :index="menuChildren_v.path">
                  <i class="is-children fa fa-circle-o"></i>
                  <span>{{menuChildren_v.name}}</span>
                </el-menu-item>
              </el-submenu>

              <el-menu-item v-else
                            :index="menu_v.path">
                <i :class="menu_v.icon"></i>
                <span>{{menu_v.name}}</span>
              </el-menu-item>

            </template>

          </el-menu>
        </div>
      </div>
      <div class="app-body">
        <div id="nav-bar"
             v-if="switchTabBar"
             :style="fixedTabBar?'position: fixed':''">
          <NavBar></NavBar>
        </div>
        <div v-else
             style="margin-top:50px;"></div>
        <div id="mainContainer"
             :style="switchTabBar&&fixedTabBar?'padding-top: 94px':''">
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';

import Menu from '@/menu/index'
import Screenfull from 'screenfull'
import NavBar from './NavBar.vue'

export default {
  //import引入的组件需要注入到对象中才能使用
  components: {
    NavBar
  },
  data () {
    //这里存放数据
    return {
      menu: Menu,
      isCollapse: false,
      switchTabBar: true,
      fixedTabBar: false,
      sysUserName: ''
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
    handleOpen (key, keyPath) {
      // console.log(key, keyPath);
    },
    handleClose (key, keyPath) {
      // console.log(key, keyPath);
    },
    NavBarWidth () {

    },

    // 全屏
    screenfullToggle () {
      if (!Screenfull.enabled) {
        this.$message({
          message: '你的浏览器不支持全屏!',
          type: 'warning'
        })
        return false
      }
      Screenfull.toggle()
    },

    saveSwitchTabBar (v) {
      v ? localStorage.setItem('switchTabBar', v) : localStorage.removeItem('switchTabBar');
    },

    saveFixedTabBar (v) {
      v ? localStorage.setItem('fixedTabBar', v) : localStorage.removeItem('fixedTabBar');
    },

    // 退出
    logout () {
      var _this = this;
      this.$confirm('确认退出吗?', '提示', {
        //type: 'warning'
      }).then(() => {
        sessionStorage.removeItem('user');
        _this.$router.push('/login');
      }).catch((err) => {
        console.log(err)
      });
    }

  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created () {
  },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted () {
    this.switchTabBar = localStorage.getItem('switchTabBar') ? true : false;
    this.fixedTabBar = localStorage.getItem('fixedTabBar') ? true : false;
    var user = sessionStorage.getItem('user');
    if (user) {
      user = JSON.parse(user);
      this.sysUserName = user.name || '';
    }
  },
  //生命周期 - 创建之前
  beforeCreate () { },
  //生命周期 - 挂载之前
  beforeMount () { },
  //生命周期 - 更新之前
  beforeUpdate () { },
  //生命周期 - 更新之后
  updated () { },
  //生命周期 - 销毁之前
  beforeDestroy () { },
  //生命周期 - 销毁完成
  destroyed () { },
  //如果页面有keep-alive缓存功能，这个函数会触发
  activated () { },
}
</script>
<style scoped>
/* @import url(); 引入公共css类 */
.main {
  display: flex;
}
.header {
  width: 100%;
  position: fixed;
  height: 50px;
  background-color: #3c8dbc;
  z-index: 10;
  display: flex;
}
.header .logo {
  background: #367fa9;
  width: 230px;
  height: 50px;
  text-align: center;
  overflow: hidden;
  line-height: 50px;
  color: #fff;
  -webkit-transition: width 0.35s;
  transition: all 0.3s ease-in-out;
}
.header .logo .big {
  display: block;
}
.header .logo .min {
  display: none;
}
.header .logo .min img {
  width: 40px;
  margin-top: 5px;
}
.header .header-btn {
  overflow: hidden;
  height: 50px;
  display: inline-block;
  text-align: center;
  line-height: 50px;
  cursor: pointer;
  padding: 0 14px;
  color: #fff;
  font-size: 16px;
}
.header .header-btn:hover {
  background-color: #367fa9;
}
.header .header-right {
  position: absolute;
  right: 0;
}
.app {
  width: 100%;
}
.app .aside {
  margin-top: 50px;
  background-color: #222d32;
  position: fixed;
  transition: all 0.3s ease-in-out;
}
.app .aside .menu {
  overflow-y: auto;
  height: calc(100vh - 50px);
}
.app .app-body {
  margin-left: 230px;
  -webkit-transition: margin-left 0.3s ease-in-out;
  transition: margin-left 0.3s ease-in-out;
}
.el-menu {
  border-right: none;
}
.menu .el-menu:not(.el-menu--collapse) {
  width: 230px;
  transition: all 0.3s linear;
  overflow-y: auto;
  height: 100%;
}
.el-menu i.fa {
  width: 24px;
  text-align: left;
}

.header-btn >>> .el-badge__content {
  top: 12px;
  border: 0;
  background-color: #00a65a;
}

.setting-category {
  padding: 10px;
  text-align: center;
  width: 330px;
}

/* 导航条 */
.fixedTabBar {
  margin-top: 10px;
}
#nav-bar {
  margin-top: 50px;
  height: 38px;
  width: 100%;
  background-color: #fff;
  z-index: 1;
}

#mainContainer {
  padding: 6px;
  background-color: #e8ecf1;
  width: 98%;
  height: 750px;
  margin: 6px;
  display: inline-block;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}
</style>
