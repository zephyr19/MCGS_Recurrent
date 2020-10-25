<template>
  <div>
    <panel class="panel" />
    <graph class="graph" />
    <!-- <div id="3d-graph" class="home"></div> -->
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import ForceGraph3D from '3d-force-graph'
import Panel from '../components/Panel/index.vue'
import Graph from '../components/Graph/index.vue'

@Component({
  components: {
    Panel,
    Graph
  }
})
export default class Home extends Vue {
  name = 'Home'
  data() {
    return {}
  }
  mounted() {
    const elem = document.getElementById('3d-graph')

    const Graph = ForceGraph3D()(elem!).jsonUrl('data/cpan.json')
  }
}
</script>

<style scoped>
.panel {
  height: 60px;
}

.graph {
  height: calc(100% - 60px - 30px);
}
</style>
