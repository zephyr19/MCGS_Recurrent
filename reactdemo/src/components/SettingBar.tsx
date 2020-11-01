import React, { useEffect } from "react";
import { Form, Select, InputNumber, Button } from "antd";
import { Settings } from "../interfaces";

const { Option } = Select;

type BarProps = {
  style: React.CSSProperties;
  onSettingBarHeight: (barHeight: number) => void;
  onLoadingOrigin: (graph: string) => void;
  onSampling: (data: Settings) => void;
};

const SettingBar = (props: BarProps) => {
  const graphList = ["Cagrqc", "Cpan", "Eurosis"];
  const algorithmList = ["BF", "FF", "MCGS", "RAS", "RDN", "RMSC", "TIES"];

  useEffect(() => {
    const formEl = document.getElementById("form");
    props.onSettingBarHeight(formEl?.clientHeight!);
  }, []);

  const onFinish = (value: any) => {
    console.log(value);
    const data: Settings = {
      graph: value.graph,
      algorithm: value.algorithm,
      params: {
        rate: value.rate,
        alpha: "0.3",
        beta: "2",
        "loss weight": "1,0,0",
      },
    };
    props.onSampling(data);
  };

  return (
    <Form
      id="form"
      size="large"
      name="info"
      initialValues={{ graph: "Cpan", algorithm: "BF", rate: "0.3" }}
      layout="inline"
      style={props.style}
      onFinish={onFinish}
    >
      <Form.Item
        label="Dataset"
        name="graph"
        rules={[{ required: true, message: "Please select a dataset" }]}
      >
        <Select
          style={{ width: 200 }}
          onChange={(graph: string) => {
            props.onLoadingOrigin(graph);
          }}
        >
          {graphList.map((graph) => (
            <Option value={graph} key={graph}>
              {graph}
            </Option>
          ))}
        </Select>
      </Form.Item>

      <Form.Item
        label="Algorithm"
        name="algorithm"
        rules={[{ required: true, message: "Please select an algorithm" }]}
      >
        <Select style={{ width: 200 }}>
          {algorithmList.map((algorithm) => (
            <Option value={algorithm} key={algorithm}>
              {algorithm}
            </Option>
          ))}
        </Select>
      </Form.Item>
      <Form.Item
        label="Sample rate"
        name="rate"
        rules={[{ required: true, message: "Please input the sample rate" }]}
      >
        <InputNumber style={{ width: 200 }} min={0} max={1} />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">
          Run
        </Button>
      </Form.Item>
    </Form>
  );
};

export default SettingBar;
