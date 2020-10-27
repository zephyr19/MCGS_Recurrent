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
    <div id="3d-graph-origin"></div>

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
import { mapState } from "vuex";
import ForceGraph3D from "3d-force-graph";

export default {
  data() {
    return {};
  },
  computed: {
    ...mapState(["dataset", "originLoading", "graphRecord"]),
    origin3DFile() {
      return `data/${this.dataset.toLowerCase()}.json`;
    }
  },
  methods: {},
  watch: {
    originLoading(newValue) {
      if (newValue) {
        const elemOrigin = document.getElementById("origin");
        const elem = document.getElementById("3d-graph-origin");
        const Graph = ForceGraph3D()(elem)
          .jsonUrl(this.origin3DFile)
          .width(elem.clientWidth)
          .height(elemOrigin.clientHeight - 40)
          .backgroundColor("white")
          .nodeAutoColorBy("id")
          .linkColor("#ccc");
        this.$store.commit("SET_ORIGINLOADING", false);
      }
    }
  }
};
</script>

<style lang="scss">
.origin {
  color: #999;
}

.origin-header {
  display: flex;
  justify-content: space-between;
  line-height: 20px;
}

.origin-tip {
  // position: absolute;
  // top: 50%;
  // left: 50%;
  // transform: translate(-50%, -50%);
}
</style>
