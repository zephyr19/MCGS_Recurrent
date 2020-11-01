// You can include shared interfaces/types in a separate file
// and then use them in any component by importing them. For
// example, to import the interface below do:
//
// import User from 'path/to/interfaces';

export type Settings = {
  graph: string;
  algorithm: string;
  params: {
    rate: string;
    alpha: string;
    beta: string;
    "loss weight": string;
  }
}

export type GraphData = {
  nodes: Array<any>;
  edges: Array<any>;
}

export type RecordData = {
  edge_num: number;
  node_num: number;
  minority: {
    "Huge Star": number[],
    "Rim": number[],
    "Super Pivot": number[],
    "Tie": number[],
  }
}