<template>
  <div id="sample" class="wrapper sample" v-loading="sampleLoading">
    <span class="sampling-header"
      >Graph Samples {{ graphRecord.node_num }}</span
    >
    <div class="sample-item-box">
      <!-- <sample-item
        v-for="i in sampleNum"
        :key="i"
        class="sample-item"
        :id="`sample${i}`"
        :graphData="graphData"
      ></sample-item> -->
      <sample-g6
        v-for="i in sampleNum"
        :key="i"
        class="sample-item"
        :id="`sample${i}`"
        :graphData="graphData"
      />
    </div>
    <i
      class="el-icon el-icon-arrow-left arrow-icon"
      v-show="sampleNum >= 3 && samping_hover && left_num !== 1"
      @click="switch_view('left')"
      style="left: 0.8%"
    ></i>
    <i
      class="el-icon el-icon-arrow-right arrow-icon"
      v-show="sampleNum >= 3 && samping_hover && right_num !== sampleNum"
      @click="switch_view('right')"
      style="right: 0.8%"
    ></i>
    <div
      v-show="sampleNum >= 2"
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

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import { State, Action, Getter } from "vuex-class";
import api from "../../api/index";
import SampleItem from "./SampleItem.vue";
import SampleG6 from "./SampleG6.vue";

@Component({
  components: {
    SampleItem,
    SampleG6
  }
})
export default class Sample extends Vue {
  sampleNum = 0;
  carouselHeight = 0;
  graphData = {};
  graphRecord = {};
  @State("sampleLoading") sampleLoading!: boolean;
  @State("dataset") graphName!: string;
  @State("algorithm") algorithm!: string;
  @State("params") params!: object;
  @Action("setSampleLoading") setSampleLoading!: (
    value: boolean
  ) => Promise<void>;

  @Watch("sampleLoading", { immediate: true, deep: true })
  onSampleLoadingChanged(newValue: boolean) {
    if (newValue) {
      api
        .runSampling({
          graphName: this.graphName,
          algorithm: this.algorithm,
          params: this.params
        })
        .then(res => {
          this.graphRecord = res.data.graph_record;
          this.graphData = res.data.graph_data;
          this.sampleNum++;
        });
      this.setSampleLoading(false);
    }
  }
}
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

.sample-header {
  line-height: 20px;
}

.sample-item-box {
  display: flex;
  flex-direction: row;
  height: calc(100% - 20px);
  justify-content: space-between;
}

.sample-item {
  width: 48%;
  height: 100%;
}
</style>
