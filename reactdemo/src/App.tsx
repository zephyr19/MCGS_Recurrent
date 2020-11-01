import React, { FC } from "react";
import "./App.css";
import { useState } from "react";
import SettingBar from "./components/SettingBar";
import Graph from "./components/Graph";
import { ShareAltOutlined } from "@ant-design/icons";
import api from "./api";
import { GraphData, RecordData, Settings } from "./interfaces";
import G6Graph from "./components/G6Graph";

const App: FC = () => {
  const [samplingList, setSamlingList] = useState<GraphData[]>([]);
  const [recordList, setRecordList] = useState<RecordData[]>([]);
  const [originData, setOriginData] = useState<GraphData>();

  const loadOrigin = (graph: string) => {
    if (graph) {
      fetch(`./data/${graph.toLocaleLowerCase()}.json`)
        .then((res) => res.json())
        .then((data) => {
          setOriginData(data);
        });
    }
  };

  const fetchData = (settings: Settings) => {
    const samplingListNew = [...samplingList];
    const recordListNew = [...recordList];
    api.runSampling(settings).then((res) => {
      console.log(res.data.graph_record);
      samplingListNew.push(res.data.graph_data);
      recordListNew.push(res.data.graph_record);
      setSamlingList(samplingListNew);
      setRecordList(recordListNew);
    });
  };

  const titleHeight = 50;
  const [barHeight, setbarHeight] = useState(70);

  return (
    <>
      <div className="header">
        <ShareAltOutlined style={{ marginRight: "10px" }} />
        Graph Sampling
      </div>
      <SettingBar
        style={{
          width: "100%",
          padding: "15px",
          border: "1px solid #ccc",
          marginTop: "15px",
        }}
        onSettingBarHeight={(barHeight) => setbarHeight(barHeight)}
        onLoadingOrigin={(graph) => loadOrigin(graph)}
        onSampling={(settings) => fetchData(settings)}
      />
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          height: `calc(100vh - ${titleHeight}px - ${barHeight}px - 30px - 15px)`,
          marginTop: "15px",
        }}
      >
        <div style={{ width: "34%", border: "1px solid #ccc" }}>
          <div style={{ color: "#999", fontSize: "1.2em", margin: "2px 8px" }}>
            Origin Graph
          </div>
          <G6Graph style={{ width: "100%" }} data={originData} id="origin" />
        </div>
        <div
          style={{
            width: "64%",
            border: "1px solid #ccc",
          }}
        >
          <div style={{ color: "#999", fontSize: "1.2em", margin: "2px 8px" }}>
            Sample Graph
          </div>
          <Graph samplingList={samplingList} recordList={recordList} />
        </div>
      </div>
    </>
  );
};

export default App;
