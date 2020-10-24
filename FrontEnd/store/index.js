export const state = () => ({
    dataset: '',
    algorithm: '',
    params: {
        'rate': '',
        'alpha': '1',
        'beta': '2',
        'loss weight': '1,0,0'
    },


    // Origin Component
    originLoading: false,
    anomalyTotal: '',
    graphRecord: '',
})

export const getters = {
}

export const mutations = {
    SET_DATASET(state, value) {
        state.dataset = value
    },
    SET_ALGORITHM(state, value) {
        state.algorithm = value
    },
    INIT_PARAMS(state, o) {
        state.params = o
    },
    SET_PARAMS(state, o) {
        state.params[o.key] = o.value
    },
    SET_ANOMALY(state, value) {
        state.anomalyTotal = value
    },
    SET_GRAPHRECORD(state, value) {
        state.graphRecord = value
    },
    SET_ORIGINLOADING(state, value) {
        state.originLoading = value
    }
}

import api from '../api/index'

export const actions = {
    clearAlgorithmSettings({ commit }) {
        commit('SET_ALGORITHM', '')
        commit('INIT_PARAMS', {
            'rate': '',
            'alpha': '1',
            'beta': '2',
            'loss weight': '1,0,0',
        })
        commit('SET_ORIGINLOADING', true)
        // self.select_minotype = '';

        // //删除采样图列表
        // self.left_num = 1;
        // self.right_num = 2;
        // self.queue_num = 0;
    },
    getGraphInfo({ state, commit }) {
        api.getGraphInfo(state.dataset).then(res => {
            commit('SET_ANOMALY', res.data.anomaly_total)
            commit('SET_GRAPHRECORD', res.data.graph_record)
        })
    }
}