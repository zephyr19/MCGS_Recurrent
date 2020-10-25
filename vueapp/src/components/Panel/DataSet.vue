<template>
  <basic title="Graph Data Set">
    <el-select
      v-model="dataset"
      placeholder="Please select Graph Data"
      @change="initOriginGraph"
    >
      <el-option
        v-for="item in datasetList"
        :key="item"
        :label="item"
        :value="item"
      >
      </el-option>
    </el-select>
  </basic>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { State, Action, Getter } from 'vuex-class';
import Basic from './basic.vue'

@Component({
  components: {
    Basic
  }
})

export default class DataSet extends Vue {
  datasetList = ['Cagrqc', 'Cpan', 'Eurosis']
  @State('dataset') datasetVuex!: string
  @Action('setDataset') setDataset!: Function
  @Action('clearAlgorithmSettings') clearAlgorithmSettings!: Function
  @Action('getGraphInfo') getGraphInfo!: Function

  get dataset(): string {
    return this.datasetVuex
    }

  set dataset(value: string) {
this.setDataset(value)
    }
    initOriginGraph() {
this.clearAlgorithmSettings()
this.getGraphInfo()
    }
}
</script>

<style></style>
