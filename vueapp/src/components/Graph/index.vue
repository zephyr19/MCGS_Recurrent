<template>
  <div class="graph">
    <origin class="origin" />
    <sample class="sample" />
  </div>
</template>

<script>
import Origin from './Origin.vue'
import Sample from './Sample.vue'

export default {
  name: 'Graph',
  components: {
    Origin,
    Sample,
  },
}
</script>

<style lang="scss" scoped>
.graph {
  display: flex;
  justify-content: space-between;
}

.origin {
  width: 38%;
}

.sample {
  width: 60%;
}
</style>
