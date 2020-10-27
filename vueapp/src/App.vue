<template>
  <div id="app">
    <div class="header"><i class="el-icon-share"></i> Graph Sampling</div>
    <router-view class="vue" />
  </div>
</template>

<style lang="scss">
.header {
  width: calc(100% - 10px);
  background-color: #ccc;
  font-size: 30px;
  font-weight: bold;
  line-height: 50px;
  color: white;
  padding-left: 10px;
}

.vue {
  height: calc(100vh - 50px - 16px);
  overflow: hidden;
}
</style>
