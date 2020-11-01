import React, { useEffect } from "react";
import G6 from "@antv/g6";
import { GraphData } from "../interfaces";

type DataProps = {
  data: GraphData | undefined;
  id: string;
  style: any;
};

const G6Graph = (props: DataProps) => {
  useEffect(() => {
    if (!props.data) return;
    const graphDiv = document.getElementById(props.id);
    const width = graphDiv!.scrollWidth;
    const height = graphDiv!.scrollHeight || 500;

    const group: Array<Array<string>> = [];
    const color: Array<string> = [];
    for (let i = 0; i < props.data.nodes.length; i++) {
      const node = props.data.nodes[i];
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
        stroke: color[node.group] + "1)",
      };
      node.size = 10;
      node.label = "id" + node.id;
      group[node.group].push(node.id);
    }

    const fisheye = new G6.Fisheye({
      r: 200,
      showLabel: true,
    });

    const graph = new G6.Graph({
      container: props.id,
      width,
      height,
      modes: {
        default: ["drag-canvas", "zoom-canvas", "drag-node", "lasso-select"],
      },
      layout: {
        type: "force",
        preventOverlap: true,
      },
      plugins: [fisheye],
    });

    graph.data(props.data);
    graph.render();

    graph.on("afterlayout", () => {
      for (let i = 0; i < group.length; i++) {
        const hull = graph.createHull({
          id: `hull${i}`,
          type: "smooth-convex",
          members: group[i],
          padding: 10,
          style: {
            fill: color[i] + "0.6)",
            stroke: color[i] + "1)",
          },
        });
        graph.on("afterupdateitem", () => {
          hull.updateData(hull.members);
        });
      }
    });
    graph.getNodes().forEach((node) => {
      node
        .getContainer()
        .getChildren()
        .forEach((shape) => {
          if (shape.get("type") === "text") shape.hide();
        });
    });
    return () => {
      graph.destroy();
    };
  }, [props.data, props.id]);

  return <div id={props.id} style={{ ...props.style, height: "100%" }}></div>;
};

export default G6Graph;
