import {ActionTree} from 'vuex';
import { RootState } from './types';

export const actions : ActionTree<any, RootState> = {
    socket_youAre({ commit }, message) {
        commit('setIdentity', message);
    },
    socket_gameState({ commit }, { state }) {
        commit('setState', state);
    },
    socket_teamList({ commit }, { teams, max_teams }) {
        commit('setTeams', { teams, max_teams });
    },
    socket_teamJoined({ commit }, data) {
        commit('teamJoin', data);
    },
    socket_boardSwitch({ commit }, data) {
        // TODO: Actually handle board types. This event doesn't currently do anything
        console.log('Switching board', data);
    },
    socket_boardCurrent({ commit }, data) {
        commit('boardCurrent', data);
        console.log('Current board', data);
    },
    socket_questionOpen({ commit }, data) {
        commit('questionOpen', data);
    },
    socket_buzzerOpen({ commit }) {
        commit('buzzerOpen');
    },
    socket_buzzerClose({ commit }, { team }) {
        commit('buzzerClose', team);
    },
    socket_teamScore({ commit }, data) {
        commit('updateScore', data);
        commit('buzzerClose', null);
    },
    socket_questionReveal({ commit }, data) {
        commit('questionReveal', data);
    },
    socket_questionClose({ commit }) {
        commit('questionClose');
        commit('buzzerClose', null);
    },
    socket_questionWager({ commit }) {
        commit('questionWager');
    },
    socket_error({ commit }, data) {
        console.error('Got error from server:', data);
    },
};
