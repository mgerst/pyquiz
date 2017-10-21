import Vue from 'vue'
import Vuex from 'vuex'
import * as getters from './getters';
import * as actions from './actions';
import * as mutations from './mutations'

Vue.use(Vuex);

const state = {
    logged_in: false,
    admin: true,
    currentTeam: 3,
    board: null,
    teams: [
        {id: 1, name: "Team 1", score: 0},
        {id: 2, name: "Team 2", score: 100},
        {id: 3, name: "Team 3", score: -500},
        {id: 4, name: "Team 4", score: 200},
    ],
    question: null,
    dailydouble: {
        active: false,
        wager: null,
        teamId: null,
    },
    buzzed: null
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