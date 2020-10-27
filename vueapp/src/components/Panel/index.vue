<template>
  <div class="wrapper bar">
    <data-set />
    <algorithm />
    <parameters />
    <el-button class="btn" @click="runSampling">Run</el-button>
  </div>
</template>

<script>
import DataSet from "./DataSet.vue";
import Algorithm from "./Algorithm.vue";
import Parameters from "./Parameters.vue";

export default {
  components: {
    DataSet,
    Algorithm,
    Parameters
  },
  methods: {
    runSampling() {
      //检测设置值是否合法
      if (!this.$store.state.dataset) {
        this.$message("Please select Graph Data Set");
        return;
      }
      if (!this.$store.state.algorithm) {
        this.$message("Please select sampling algorithm");
        return;
      }
      const params = this.$store.state.params;
      for (const index in params) {
        if (!params[index]) {
          this.$message("Please set parameter - " + index);
          return;
        } else {
          const paramValue = params[index];
          if (
            index === "rate" &&
            (!/^[0-9]*\.{0,1}[0-9]*$/.test(paramValue) ||
              !(parseFloat(paramValue) > 0 && parseFloat(paramValue) < 1))
          ) {
            this.$message.error("Please set valid parameter - " + index);
            return;
          } else if (
            index === "alpha" &&
            (!/^[0-9]*\.{0,1}[0-9]*$/.test(paramValue) ||
              parseFloat(paramValue) < 1)
          ) {
            this.$message.error("Please set valid parameter - " + index);
            return;
          } else if (
            index === "beta" &&
            (!/^[0-9]*\.{0,1}[0-9]*$/.test(paramValue) ||
              !(parseFloat(paramValue) >= 1))
          ) {
            this.$message.error("Please set valid parameter - " + index);
            return;
          } else if (
            index === "loss weight" &&
            !/^[0-9]*\.{0,1}[0-9]*.{1}[0-9]*\.{0,1}[0-9]*.{1}[0-9]*\.{0,1}[0-9]*$/.test(
              paramValue
            )
          ) {
            this.$message.error("Please set valid parameter - " + index);
            return;
          }
        }
      }

      this.$store.commit("SET_SAMPLELOADING", true);
    }
  }
};
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
