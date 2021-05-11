<template>
  <div class="CashFlow">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>资金报表</el-breadcrumb-item>
      <el-breadcrumb-item>资金流水</el-breadcrumb-item>
    </el-breadcrumb>
    <el-divider></el-divider>
    <div class="block">
      <el-date-picker
        v-model="value1"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期">
      </el-date-picker>
<!--      <el-input v-model="input" placeholder="商户号"></el-input>-->
<!--      <el-input v-model="input" placeholder="系统订单号"></el-input>-->
<!--      <el-input v-model="input" placeholder="上游订单号"></el-input>-->
<!--      <el-input v-model="input" placeholder="订单号"></el-input>-->
      <el-select v-model="value" placeholder="商户号">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
      <el-select v-model="value" placeholder="系统订单号">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
      <el-select v-model="value" placeholder="上游订单号">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
      <el-select v-model="value" placeholder="订单号">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
    </div>
    <div>
      <el-select v-model="value" placeholder="总代理订单">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
      <el-select v-model="value" placeholder="代理订单">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
      <el-select v-model="value" placeholder="-支付方式-">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
<!--      <el-switch-->
<!--        v-model="swithValue">-->
<!--      </el-switch>-->
      <el-button type="primary" icon="el-icon-search" size="medium">搜索</el-button>
    </div>
    <div>
      <el-table
        :data="tableData"
        border
        style="width: 100%">
        <el-table-column
          prop="date"
          label="商户"
          width="100">
        </el-table-column>
        <el-table-column
          prop="name"
          label="商户订单号"
          width="120">
        </el-table-column>
        <el-table-column
          prop="address"
          label="服务器订单号">
        </el-table-column>
        <el-table-column
          prop="address"
          label="订单金额">
        </el-table-column>
        <el-table-column
          prop="address"
          label="创建时间">
        </el-table-column>
        <el-table-column
          prop="address"
          label="变动前金额">
        </el-table-column>
        <el-table-column
          prop="address"
          label="变动后金额">
        </el-table-column>
        <el-table-column
          prop="address"
          label="通道">
        </el-table-column>
        <el-table-column
          prop="address"
          label="变动类型">
        </el-table-column>
        <el-table-column
          prop="address"
          label="操作说明">
        </el-table-column>
      </el-table>
    </div>
    <div>
      <el-pagination
        background
        layout="prev, pager, next"
        :total="1">
      </el-pagination>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      swithValue:true,
    }
  }
}
</script>
<style lang="scss" scoped>
  .CashFlow{
    .block{
      display: flex;
    }
  }
</style>
