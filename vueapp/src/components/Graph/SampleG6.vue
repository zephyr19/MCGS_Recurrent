<template>
  <div :id="id"></div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import G6 from "@antv/g6";

interface GraphData {
  nodes: Array<any>;
  edges: Array<any>;
}

@Component
export default class SampleG6 extends Vue {
  @Prop(String) readonly id!: string;
  @Prop(Object) readonly graphData!: GraphData;

  mounted() {
    const data = this.graphData;
    console.log("SampleItem G6 say hi");
    console.log(data);
    const graphDiv = document.getElementById(this.id);

    const width = graphDiv!.scrollWidth;
    const height = graphDiv!.scrollHeight || 500;

    const group: Array<Array<string>> = [];
    const color: Array<string> = [];
    for (let i = 0; i < data.nodes.length; i++) {
      const node = data.nodes[i];
      if (group[node.group] == null) {
        group[node.group] = [];
        const randomColor =
          "rgba(" +
          Math.random() * 255 +
          ", " +
          Math.random() * 255 +
          ", " +
          Math.random() * 255 +
          ", ";
        color[node.group] = randomColor;
      }
      node.style = {
        fill: color[node.group] + "0.8)",
        stroke: color[node.group] + "1)"
      };
      node.size = 10;
      node.label = "id" + node.id;
      group[node.group].push(node.id);
    }

    const fisheye = new G6.Fisheye({
      r: 200,
      showLabel: true
    });

    const graph = new G6.Graph({
      container: this.id,
      width,
      height,
      modes: {
        default: ["drag-canvas", "zoom-canvas", "drag-node", "lasso-select"]
      },
      layout: {
        type: "force",
        preventOverlap: true
      },
      plugins: [fisheye]
    });
    graph.data(data);
    graph.render();

    graph.on("afterlayout", () => {
      for (let i = 0; i < group.length; i++) {
        console.log(`hull${i}`);
        console.log(group[i]);
        const hull = graph.createHull({
          id: `hull${i}`,
          type: "smooth-convex",
          members: group[i],
          padding: 10,
          style: {
            fill: color[i] + "0.6)",
            stroke: color[i] + "1)"
          }
        });
        graph.on("afterupdateitem", () => {
          hull.updateData(hull.members);
        });
      }
    });
    graph.getNodes().forEach(node => {
      node
        .getContainer()
        .getChildren()
        .forEach(shape => {
          if (shape.get("type") === "text") shape.hide();
        });
    });
  }
}
</script>
