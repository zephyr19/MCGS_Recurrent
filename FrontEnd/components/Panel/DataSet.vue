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

<script>
import basic from './basic.vue'

export default {
  name: 'DataSet',
  components: {
    basic,
  },
  data() {
    return {
      datasetList: ['Cagrqc', 'Cpan', 'Eurosis'],
    }
  },
  computed: {
    dataset: {
      get() {
        return this.$store.state.dataset
      },
      set(value) {
        this.$store.commit('SET_DATASET', value)
      },
    },
  },
  methods: {
    initOriginGraph() {
      this.$store.dispatch('clearAlgorithmSettings')
      // d3.selectAll('.sampling-item').remove();
      this.$store.dispatch('getGraphInfo')
    },
  },
}
</script>

<style></style>
