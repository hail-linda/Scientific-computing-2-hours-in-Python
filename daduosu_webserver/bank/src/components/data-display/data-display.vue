<!--  -->
<template>
  <div class='data-display'>
    <el-row :span="24">
      <el-col v-for="(item,index) in data"
              :key="index"
              :span="span">
        <div class="item"
             :style="{color:color}">
          <h5 class="count">
            <CountUp :start="14"
                     :end="item.count">{{item.count}}</CountUp>
          </h5>
          <span class="splitLine"></span>
          <p class="title">{{item.title}}</p>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import CountUp from '@/components/count-up/index.vue'

export default {
  //import引入的组件需要注入到对象中才能使用
  components: { CountUp },
  data () {
    //这里存放数据
    return {
      span: this.option.span || 8,
      data: this.option.data,
      color: this.option.color || 'rgb(63, 161, 255)'
    };
  },
  props: {
    option: {
      type: Object,
      default: () => { }
    }
  },


  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {

  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created () {

  },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted () {

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
.item {
  display: flex;
  align-items: center;
  flex-direction: column;
  margin: 5px 0;
  text-align: center;
}

.count {
  margin: 8px 0;
  font-weight: bold;
  font-size: 32px;
  color: #15a0ff;
}

.title {
  color: #999;
}

.splitLine {
  display: block;
  margin: 0 auto;
  width: 24px;
  height: 1px;
  background: #9b9b9b;
}
</style>