import { LeftOutlined, RightOutlined } from "@ant-design/icons";
import { Button, Divider } from "antd";
import React, { useEffect, useState } from "react";
import G6Graph from "./G6Graph";

type GraphProps = {
  samplingList: Array<any>;
  recordList: Array<any>;
};

const Graph = (props: GraphProps) => {
  const len = props.samplingList.length;
  let [cur, setCur] = useState(1);

  useEffect(() => {
    setCur(len - 1);
  }, [props.samplingList, props.recordList]);

  if (len === 1) {
    return (
      <G6Graph
        style={{ width: "49%" }}
        data={props.samplingList[0]}
        key={`sample${0}`}
        id={`sample${0}`}
      />
    );
  } else if (len > 1) {
    return (
      <div
        style={{
          width: "100%",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          overflow: "hidden",
        }}
      >
        <Button
          type="text"
          icon={<LeftOutlined />}
          size="small"
          onClick={() => {
            setCur(cur + 1);
          }}
        />
        <G6Graph
          style={{ width: "46%" }}
          data={props.samplingList[cur]}
          key={`sample${cur}`}
          id={`sample${cur}`}
        />
        <Divider dashed type="vertical" style={{ height: "100%" }} />
        <div style={{ width: "46%", height: "100%" }}>
          {props.recordList[cur - 1]}
          <G6Graph
            style={{ width: "100%" }}
            data={props.samplingList[cur - 1]}
            key={`sample${cur - 1}`}
            id={`sample${cur - 1}`}
          />
        </div>
        <Button
          type="text"
          icon={<RightOutlined />}
          size="small"
          onClick={() => setCur(cur - 1)}
        />
      </div>
    );
  }
  return <div></div>;
};

export default Graph;
