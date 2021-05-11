<!--  -->
<template>
  <div class='nav-bar'>
    <ScrollPane class="nav-bar-scroll">
      <router-link :to="tag.path"
                   :key="tag.path"
                   class="nav-bar-tag"
                   :class="isActive(tag)?'active':''"
                   tag="a"
                   v-for="tag in Array.from(visitedViews)">
        {{ tag.title }}
        <div class="close-box"
             v-show="list!=1">
          <span class="el-icon-close"
                @click.prevent.stop='closeSelectedTag(tag)'></span>
        </div>
      </router-link>
    </ScrollPane>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';

import ScrollPane from '@/components/ScrollPane.vue'

export default {
  name: 'tagsView',
  //import引入的组件需要注入到对象中才能使用
  components: { ScrollPane },
  data () {
    //这里存放数据
    return {
      list: ''
    };
  },
  //监听属性 类似于data概念
  computed: {
    visitedViews () {
      const list = this.$store.state.tagsView.visitedViews.length
      this.list = list
      return this.$store.state.tagsView.visitedViews
    }
  },
  //监控data中的数据变化
  watch: {
    $route () {
      this.addViewTags()
    }
  },
  //方法集合
  methods: {
    generateRoute () {
      if (this.$route.name) {
        return this.$route
      }
      return false
    },
    // 碰到是否是当前页面
    isActive (route) {
      return route.path == this.$route.path
    },
    // 添加到tags
    addViewTags () {
      const route = this.generateRoute()
      if (!route) {
        return false
      }
      this.$store.dispatch('addVisitedViews', route)
    },
    // 关闭页面
    closeSelectedTag (view) {
      this.$store.dispatch('delVisitedViews', view).then((views) => {
        if (this.isActive(view)) {
          const latestView = views.slice(-1)[0]
          if (latestView) {
            this.$router.push(latestView.path)
          }
        }
      })
    }

  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created () {

  },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted: function () {
    this.addViewTags()
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
.nav-bar {
  padding: 0 4px;
  height: 38px;
}
.nav-bar-tag {
  height: 26px;
  color: #495060;
  margin: 6px 2px;
  padding-left: 6px;
  padding-right: 6px;
  font-size: 12px;
  line-height: 26px;
  border: 1px solid #ebeef5;
  border-radius: 2px;
  display: inline-block;
  cursor: pointer;
}
.nav-bar-tag.active {
  background-color: #3c8dbc;
  color: #fff;
  border-color: #3c8dbc;
}
.close-box {
  display: inline-block;
  height: 100%;
  border-left: 1px solid #ebeef5;
  margin-left: 6px;
}
.close-box .el-icon-close {
  font-weight: bolder;
  margin-left: 6px;
}
.close-box .el-icon-close:hover {
  color: #f40;
}

.nav-bar-scroll {
  flex: 1;
  height: 100%;
}
</style>