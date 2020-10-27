<template>
  <div>
    <panel class="panel" />
    <graph class="graph" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Panel from "../components/Panel/index.vue";
import Graph from "../components/Graph/index.vue";

@Component({
  components: {
    Panel,
    Graph
  }
})
export default class Home extends Vue {}
</script>

<style scoped>
.panel {
  height: 60px;
}

.graph {
  height: calc(100% - 60px - 45px);
  overflow: hidden;
}
</style>
