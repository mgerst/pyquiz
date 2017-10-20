import Vue from 'vue'
import Vuex from 'vuex'
import * as getters from './getters';
import * as mutations from './mutations'

Vue.use(Vuex);

const state = {
    admin: true,
    currentTeam: 3,
    board: {
        categories: ["A", "B", "C", "D", "E", "F"],
        items: {
          "A": [
            {value: 100, show: true, category: "A", clue: "This is a test question", answer: "Test answer"},
            {value: 200, show: true, category: "A", dailydouble: true, clue: "Again with the clue", answer: "Another answer"},
            {value: 300, show: true, category: "A"},
            {value: 400, show: true, category: "A"},
            {value: 500, show: true, category: "A"}
          ],
          "B": [
            {value: 100, show: true, category: "B"},
            {value: 200, show: true, category: "B"},
            {value: 300, show: true, category: "B"},
            {value: 400, show: true, category: "B"},
            {value: 500, show: true, category: "B"}
          ],
          "C": [
            {value: 100, show: true, category: "C"},
            {value: 200, show: true, category: "C"},
            {value: 300, show: true, category: "C"},
            {value: 400, show: true, category: "C"},
            {value: 500, show: true, category: "C"}
          ],
          "D": [
            {value: 100, show: true, category: "D"},
            {value: 200, show: true, category: "D"},
            {value: 300, show: true, category: "D"},
            {value: 400, show: true, category: "D"},
            {value: 500, show: true, category: "D"}
          ],
          "E": [
            {value: 100, show: true, category: "E"},
            {value: 200, show: true, category: "E"},
            {value: 300, show: true, category: "E"},
            {value: 400, show: true, category: "E"},
            {value: 500, show: true, category: "E"}
          ],
          "F": [
            {value: 100, show: true, category: "F"},
            {value: 200, show: true, category: "F"},
            {value: 300, show: true, category: "F"},
            {value: 400, show: true, category: "F"},
            {value: 500, show: true, category: "F"}
          ],
        }
    },
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
    getters,
    mutations
});

if (module.hot) {
    module.hot.accept([
        './getters',
        './mutations'
    ], () => {
        store.hotUpdate({
            mutations: require('./mutations')
        })
    })
}

export default store;