// types.ts
export interface ParamsInfo {
  rate: string;
  alpha: string;
  beta: string;
  "loss weight": string;
}

export interface RootState {
  dataset: string;
  algorithm: string;
  params: ParamsInfo;
  originLoading: boolean;
  anomalyTotal: object;
  graphRecord: object;
}
