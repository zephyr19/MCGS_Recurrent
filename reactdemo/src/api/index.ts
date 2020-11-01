import axios from "axios";
import { Settings } from "../interfaces";

const apiClient = axios.create({
  baseURL: `http://localhost:8000`,
  withCredentials: false, // This is the default
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json"
  }
});

interface GraphInfoParams {
  graphName: string;
}

const api = {
  getGraphInfo(params: GraphInfoParams) {
    return apiClient.post("/getGraphInfo/", params);
  },

  runSampling(params: Settings) {
    return apiClient.post("/runSampling/", params);
  }
};

export default api
