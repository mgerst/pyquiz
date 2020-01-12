import { MutationTree } from 'vuex';
import { RootState, State, Question, Category } from './types';

export const mutations : MutationTree<RootState> = {
    setIdentity(state, { admin, team, logged_in }) {
        state.admin = admin;
        state.team = team;
        state.logged_in = logged_in;
    },
    setState(state, gameState : State) {
        state.state = gameState;
    },
    setTeams(state, { teams, max_teams}) {
        state.teams = teams;
        state.max_teams = max_teams;
    },
    teamJoin(state, { team, name }) {
        const found_team = state.teams.find(t => team === t.id);
        found_team!.taken = true;
        found_team!.name = name;
    },
    boardCurrent(state, data) {
        state.board = data;
    },
    questionOpen(state, { question, category, clue, value, daily_double, type }) {
        state.currentQuestion = {
            id: question,
            category: category,
            clue: clue,
            value: value,
            answer: null,
            daily_double: daily_double,
            wager: null,
            type: type,
        };
    },
    questionReveal(state, { answer }) {
        state.currentQuestion!.answer = answer;
    },
    buzzerOpen(state) {
        state.buzzer = true;
        state.buzzedTeam = null;
    },
    buzzerClose(state, team : number | null) {
        state.buzzer = false;
        state.buzzedTeam = team;
    },
    updateScore(state, { team, score }) {
        state.teams.find(t => t.id === team)!.score = score;
    },
    questionClose(state) {
        const cat_id = state.currentQuestion!.category;
        const q_id = state.currentQuestion!.id;
        state.currentQuestion = null;

        const category = state.board!.categories.find(cat => cat.id === cat_id)!;
        const question = category!.questions.find(ques => ques.id === q_id)!;
        if (question) {
            question.visible = false;
        }
    },
    questionWager(state) {
        if (!state.admin || !state.currentQuestion!.wager) {
            state.currentQuestion!.wager = true;
        }
    },
};
