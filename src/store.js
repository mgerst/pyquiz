import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    admin: true,
    currentTeam: 3,
    board: {
      categories: ["A", "B", "C", "E", "F", "G"],
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
        "G": [
          {value: 100, show: true, category: "G"},
          {value: 200, show: true, category: "G"},
          {value: 300, show: true, category: "G"},
          {value: 400, show: true, category: "G"},
          {value: 500, show: true, category: "G"}
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
  },
  mutations: {
    openQuestion(state, {value, category}) {
      if (state.question !== null) {
        console.error("Opened question when another question is already open!");
      }

      let item = state.board.items[category].find(item => item.value === value);
      item.show = false;

      state.question = item;
      state.dailydouble.active = item.dailydouble || false;
    },
    closeQuestion(state) {
      state.question = null;
      if (state.dailydouble.active) {
        state.dailydouble = {
          active: false,
          teamId: null,
          wager: null,
        }
      }
      state.buzzed = null;
    },
    modifyScore(state, {teamId, value}) {
      let team = state.teams.find(team => {
        return teamId === team.id
      });

      let score = state.question.value;
      if (state.dailydouble.active && teamId === state.dailydouble.teamId) {
        score = state.dailydouble.wager;
      }

      // This will take care of negative vs positive
      score *= value;
      team.score += score;
      state.buzzed = null;

      if (value > 0) {
        this.commit('closeQuestion');
      }
    },
    setAdmin(state, {value}) {
      state.admin = value;
    },
    setWager(state, {teamId, wager}) {
      state.dailydouble.wager = wager;
      state.dailydouble.teamId = teamId;
    },
    setBuzzed(state) {
      if (state.buzzed !== null) {
        return;
      }

      state.buzzed = state.currentTeam;
    },
    clearBuzzed(state) {
      state.buzzed = null;
    }
  },
  actions: {},
  getters: {
    categories(state) {
      return state.board.categories;
    },
    cells(state) {
      return state.board.items;
    },
    teams(state) {
      return state.teams;
    },
    isQuestionOpen(state) {
      return state.question !== null;
    },
    openQuestion(state) {
      return state.question;
    },
    isDailyDouble(state) {
      return state.dailydouble.active;
    },
    hasWager(state) {
      return state.dailydouble.active && state.dailydouble.wager !== null;
    },
    isAdmin(state) {
      return state.admin;
    },
    buzzedTeam(state) {
      return state.buzzed;
    },
    currentTeam(state) {
      return state.currentTeam;
    }
  }
});