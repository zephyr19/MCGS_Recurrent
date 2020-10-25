<template>
  <div id="origin" class="wrapper origin" v-loading="originLoading">
    <div class="origin-header">
      <span class="origin-title">original graph</span>
      <span class="origin-info" v-show="graphRecord.edge_num"
        ><b>Edges:</b>{{ graphRecord.edge_num }} <b>Nodes:</b
        >{{ graphRecord.node_num }}</span
      >
    </div>
    <span class="origin-tip" v-show="dataset === ''"
      >please select graph data set</span
    >

    <!-- <div
      role="tooltip"
      id="no_tip"
      aria-hidden="false"
      class="el-popover el-popper el-popover--plain my-no-tip"
      tabindex="0"
      x-placement="bottom"
    >
      there are no <b>{{ select_minotype }}s</b> in this graph
    </div> -->
  </div>
</template>

<script>
import { mapState } from 'vuex'
// import ForceGraph3D from '3d-force-graph'

export default {
  data() {
    return {}
  },
  computed: {
    ...mapState(['dataset', 'originLoading', 'graphRecord']),
    originFisheyeFile() {
      return `json_files/origin_${this.dataset.toLowerCase()}.json`
    },
    origin3DFile() {
      return `json_files/cpan.json`
    },
    samplingFisheyeFile() {
      return 'json_files/sampling_result.json'
    },
  },
  methods: {
  },
  watch: {
  },
}
</script>

<style lang="scss">
.origin {
  color: #999;
}

.origin-header {
  display: flex;
  justify-content: space-between;
}

.origin-tip {
  // position: absolute;
  // top: 50%;
  // left: 50%;
  // transform: translate(-50%, -50%);
}
</style>
