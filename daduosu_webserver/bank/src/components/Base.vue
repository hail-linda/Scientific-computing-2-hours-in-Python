<template>
  <el-container style="border: 1px solid #eee">
    <el-aside width="320px" style="background-color: rgb(238, 241, 246)">
      <span class="user">贵宾</span>
      <el-menu
        default-active="$route.path"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b">
        <el-submenu v-for="item in menuList" :index="item.index">
          <template slot="title">
            <i :class="item.icon"></i>
            <span>{{ item.content }}</span>
          </template>
          <el-menu-item-group>
            <el-menu-item
              v-for="ite in item.submenuList"
              :index="ite.index"
            >{{ ite.subContent }}
            </el-menu-item>
          </el-menu-item-group>
        </el-submenu>
      </el-menu>

    </el-aside>
    <el-container>
      <el-header style="text-align: left; font-size: 20px">
        <el-container>
          <el-aside style="width: 40px">
            <i class="el-icon-d-arrow-left" style="position: relative;top: 8px;"></i>
          </el-aside>
          <el-tabs v-model="activeIndex" type="border-card">
            <el-tab-pane
              label="1"
              name="2"
              closable
            >
            </el-tab-pane>
          </el-tabs>
        </el-container>
      </el-header>
    </el-container>
  </el-container>
</template>
<script>
export default {
  data() {
    return {
      menuList: [{
        index: "1",
        content: "商户资料",
        icon: "el-icon-user",
        submenuList: [{subContent: "基本资料", index: "page1"},
          {subContent: "商户产品", index: "page2"},
          {subContent: "修改密码", index: "page3"},
          {subContent: "谷歌验证码绑定", index: "page4"}]
      }, {
        index: "2",
        content: "数据管理",
        icon: "el-icon-s-data",
        submenuList: []
      }, {
        index: "3",
        content: "下发管理",
        icon: "el-icon-share",
        submenuList: []
      }, {
        index: "4",
        content: "充值管理",
        icon: "el-icon-coin",
        submenuList: []
      }, {
        index: "5",
        content: "内充管理",
        icon: "el-icon-wallet",
        submenuList: []
      }, {
        index: "6",
        content: "报表管理",
        icon: "el-icon-data-analysis",
        submenuList: []
      }, {
        index: "7",
        content: "接入管理",
        icon: "el-icon-link",
        submenuList: []
      }],
      activeIndex: '1'
    }
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    }
  }
}
</script>
<style lang="scss" scoped>
.user {
  display: block;
  background-color: #545c64;
  height: 40px;
  width: 319px;
  color: #fff;
}
</style>
