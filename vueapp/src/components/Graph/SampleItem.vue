<template>
  <div :id="id"></div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import ForceGraph3D from "3d-force-graph";

interface GraphData {
  nodes: Array<any>;
  links: Array<any>;
}

@Component
export default class SampleItem extends Vue {
  @Prop(String) readonly id!: string;
  @Prop(Object) readonly graphData!: GraphData;
  mounted() {
    console.log("SampleItem say hi");
    const elem = document.getElementById(this.id);
    console.log(elem!.clientHeight);
    console.log(elem!.clientWidth);
    const Graph = ForceGraph3D()(elem!)
      .graphData(this.graphData)
      .width(elem!.clientWidth)
      .height(elem!.clientHeight)
      .nodeAutoColorBy("id")
      .backgroundColor("white")
      .linkColor("#ccc");
  }
}
</script>

<style>
</style>