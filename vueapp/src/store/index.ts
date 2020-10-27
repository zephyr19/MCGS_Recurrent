import Vue from "vue";
import Vuex, { StoreOptions } from "vuex";
import { RootState } from "./types";
import api from "../api/index";

Vue.use(Vuex);

const store: StoreOptions<RootState> = {
  state: {
    dataset: "Cpan",
    algorithm: "BF",
    params: {
      rate: "0.3",
      alpha: "1",
      beta: "2",
      "loss weight": "1,0,0"
    },

    // Origin Component
    originLoading: false,
    anomalyTotal: {},
    graphRecord: {},

    sampleLoading: false,
  },

  mutations: {
    SET_DATASET(state, value) {
      state.dataset = value;
    },
    SET_ALGORITHM(state, value) {
      state.algorithm = value;
    },
    INIT_PARAMS(state, o) {
      state.params = o;
    },
    SET_PARAMS(state, o) {
      state.params[o.key] = o.value;
    },
    SET_ANOMALY(state, value) {
      state.anomalyTotal = value;
    },
    SET_GRAPHRECORD(state, value) {
      state.graphRecord = value;
    },
    SET_ORIGINLOADING(state, value) {
      state.originLoading = value;
    },
    SET_SAMPLELOADING(state, value) {
      state.sampleLoading = value;
    }
  },
  actions: {
    setDataset({ commit }, val) {
      commit("SET_DATASET", val);
    },
    setSampleLoading({ commit }, val) {
      commit("SET_SAMPLELOADING", val);
    },
    clearAlgorithmSettings({ commit }) {
      commit("SET_ALGORITHM", "");
      commit("INIT_PARAMS", {
        rate: "",
        alpha: "1",
        beta: "2",
        "loss weight": "1,0,0"
      });
      commit("SET_ORIGINLOADING", true);
      // self.select_minotype = '';

      // //删除采样图列表
      // self.left_num = 1;
      // self.right_num = 2;
      // self.queue_num = 0;
    },
    getGraphInfo({ state, commit }) {
      api.getGraphInfo({ graphName: state.dataset }).then(res => {
        commit("SET_ANOMALY", res.data.anomaly_total);
        commit("SET_GRAPHRECORD", res.data.graph_record);
      });
    },
    checkParams(state) {
      console.log("Checking params");
      if (!state.dataset) {
        console.log("No dataset")
        return { message: 'Please select Graph Data Set' }
      }
    }
  },
  modules: {}
};

export default new Vuex.Store<RootState>(store);
