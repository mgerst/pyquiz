import Vue from 'vue'
import Vuex from 'vuex'
import { RootState, State } from './types';
import { getters } from './getters';
import { actions } from './actions';
import { mutations } from './mutations'

Vue.use(Vuex);

const state : RootState = {
    state: State.Unknown,
    admin: false,
    team: null,
    logged_in: false,
    teams: [],
    max_teams: 0,
    board: null,
    currentQuestion: null,
    buzzer: false,
    buzzedTeam: null,
};

const store = new Vuex.Store<RootState>({
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