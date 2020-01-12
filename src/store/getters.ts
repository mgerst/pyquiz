import { GetterTree } from 'vuex';
import {RootState, State, Team, Board, Question} from './types';

export const getters : GetterTree<any, RootState> = {
    gameState(state) : State {
        return state.state;
    },
    loggedIn(state) : boolean {
        return state.logged_in || window.jeopardy.observer;
    },
    isAdmin(state) : boolean {
        return state.admin;
    },
    teamList(state) : Team[] {
        return state.teams;
    },
    teamCount(state) : number {
        return state.teams ? state.teams.length : 0;
    },
    maxTeams(state) : number {
        return state.max_teams;
    },
    getTeam(state) {
        return (id : number) : Team | null => {
            if (state.teams !== null) {
                return state.teams.find(team => team.id === id);
            } else {
                return null;
            }
        };
    },
    currentTeam(state, getters) : Team | null {
        return getters.getTeam(state.team);
    },
    currentBoard(state) : Board {
        return state.board;
    },
    getQuestion(state) {
        return (cat_id : number, ques_id : number) : Question | null => {
            const category = state.board.categories.find(cat => cat.id === cat_id);
            if (!category) {
                return null;
            }

            const question = category.questions.find(ques => ques.id === ques_id);
            return question;
        };
    },
    openQuestion(state) : Question {
        return state.currentQuestion;
    },
    isQuestionOpen(state) : boolean {
        return state.currentQuestion !== null;
    },
    buzzerOpen(state) : boolean {
        return state.buzzer;
    },
    buzzedTeamId(state) : number {
        return state.buzzedTeam;
    },
    buzzedTeam(state) : Team | null {
        return state.teams.find(t => t.id === state.buzzedTeam);
    },
    questionRevealed(state) : boolean {
        if (state.currentQuestion === null) { return false; }

        return state.currentQuestion.answer !== null;
    },
    isDailyDouble(state) : boolean {
        if (state.currentQuestion === null) { return false; }

        return state.currentQuestion.daily_double;
    },
    hasWager(state) : boolean {
        if (state.currentQuestion === null) { return false; }

        return !!state.currentQuestion.wager;
    },
};
