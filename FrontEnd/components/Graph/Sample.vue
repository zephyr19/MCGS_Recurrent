<template>
  <div class="wrapper sample">
    <span id="sampling-tag">Graph Samples</span>
    <div
      class="loading-div"
      v-show="LoadingSampling"
      v-loading="LoadingSampling"
      style="left: 1%"
    ></div>
    <i
      class="el-icon el-icon-arrow-left arrow-icon"
      v-show="queue_num >= 3 && samping_hover && left_num !== 1"
      @click="switch_view('left')"
      style="left: 0.8%"
    ></i>
    <i
      class="el-icon el-icon-arrow-right arrow-icon"
      v-show="queue_num >= 3 && samping_hover && right_num !== queue_num"
      @click="switch_view('right')"
      style="right: 0.8%"
    ></i>
    <div
      v-show="queue_num >= 2"
      style="
        position: absolute;
        left: 50%;
        top: 4%;
        width: 1px;
        height: 93%;
        border-right: 1px dashed #cccccc;
      "
    ></div>
  </div>
</template>

<script>
export default {}
</script>

<style lang="scss" scpoed>
.arrow-icon {
  color: #999999;
  font-size: 25px;
  z-index: 2000;
  cursor: pointer;
  position: absolute;
  top: 45%;
}
</style>
