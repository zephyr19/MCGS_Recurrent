<template>
  <basic title="Algorithm">
    <el-select v-model="algorithm" placeholder="Please select algorithm">
      <el-option
        v-for="item in algorithmList"
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
  name: 'Algorithm',
  components: {
    basic,
  },
  data() {
    return {
      algorithmList: ['BF', 'FF', 'MCGS', 'RAS', 'RDN', 'RMSC', 'TIES'],
    }
  },
  computed: {
    algorithm: {
      get() {
        return this.$store.state.algorithm
      },
      set(value) {
        this.$store.commit('SET_ALGORITHM', value)
      },
    },
  },
}
</script>

<style></style>
