import Vue from 'vue'
import Vuex from 'vuex'
import * as getters from './getters';
import * as actions from './actions';
import * as mutations from './mutations'

Vue.use(Vuex);

const state = {
    state: 'unknown',
    admin: false,
    team: null,
    logged_in: false,
    teams: null,
    max_teams: 0,
    board: null,
    currentQuestion: null,
    buzzer: false,
    buzzedTeam: null,
};

const store = new Vuex.Store({
    state,
    actions,
    getters,
    mutations
});

if (module.hot) {
    module.hot.accept([
        './getters',
        './actions',
        './mutations'
    ], () => {
        store.hotUpdate({
            getters: require('./getters'),
            actions: require('./actions'),
            mutations: require('./mutations')
        })
    })
}

export default store;