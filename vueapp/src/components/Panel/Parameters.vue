<template>
  <basic title="Parameters">
    <div class="params-box">
      <div class="box-title">sampling rate</div>
      <el-input v-model="rate" clearable> </el-input>
      <div class="other_options">
        <div
          class="option_item"
          v-for="(option, index) in optionLabels"
          :key="index"
        >
          <el-divider direction="vertical"></el-divider>
          <span>{{ option }}</span>
          <!-- <input
            class="option_input"
            type="text"
            v-model="option"
          /> -->
        </div>
      </div>
    </div></basic
  >
</template>

<script>
import basic from "./basic.vue";

export default {
  name: "Params",
  components: {
    basic
  },
  data() {
    return {
      datasetList: ["Cagrqc", "Cpan", "Eurosis"]
    };
  },
  computed: {
    rate: {
      get() {
        return this.$store.state.params["rate"];
      },
      set(value) {
        this.$store.commit("SET_PARAMS", { key: "rate", value: value });
      }
    },
    optionLabels() {
      if (this.$store.state.algorithm == "MCGS") {
        return ["alpha", "beta", "loss weight"];
      } else {
        return [];
      }
    }
    // 'params[option]': {

    // },
    // option: {
    //   get() {
    //     this.$store.state.params[]
    //   }
    // }
  }
};
</script>

<style lang="scss" scoped>
.params-box {
  display: flex;
  align-items: center;
}

.box-title {
  color: #ccc;
  width: 100%;
}
</style>
