<template>
  <div class="container">
    <panel class="panel" />
    <graph class="graph" />
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Panel from '../components/Panel/index.vue'
import Graph from '../components/Graph/index.vue'

export default Vue.extend({
  name: 'index',
  components: {
    Panel,
    Graph,
  },
})
</script>

<style>
.container {
  /* padding: 15px; */
}

.panel {
  height: 60px;
}

.graph {
  height: calc(100% - 60px - 30px);
}
</style>
