<template>
  <div class="wrapper bar">
    <data-set />
    <algorithm />
    <parameters />
    <el-button class="btn">Run</el-button>
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
