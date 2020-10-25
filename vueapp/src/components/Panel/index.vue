<template>
  <div class="wrapper bar">
    <data-set />
    <algorithm />
    <parameters />
    <el-button class="btn" @click="runSampling">Run</el-button>
  </div>
</template>

<script>
import DataSet from './DataSet.vue'
import Algorithm from './Algorithm.vue'
import Parameters from './Parameters.vue'

export default {
  components: {
    DataSet,
    Algorithm,
    Parameters,
  },
  methods: {
    runSampling() {
      this.$message('这是一条消息提示')
      this.$store.dispatch('checkParams')
    },
  },
}
</script>

<style lang="scss" scoped>
.bar {
  display: flex;
  align-items: center;
}

.btn {
  align-self: center;
}
</style>
