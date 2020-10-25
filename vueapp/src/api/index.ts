import axios from "axios";

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

export default {
  getGraphInfo(params: GraphInfoParams) {
    return apiClient.post("/getGraphInfo/", params);
  }
};
