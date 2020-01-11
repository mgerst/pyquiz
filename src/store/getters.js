export const gameState = (state) => {
    return state.state;
};

export const loggedIn = (state) => {
    return state.logged_in || window.jeopardy.observer;
};

export const isAdmin = (state) => {
    return state.admin;
};

export const teamList = (state) => {
    return state.teams;
};

export const teamCount = (state) => {
    return state.teams ? state.teams.length : 0;
};

export const maxTeams = (state) => {
    return state.max_teams;
};

export const getTeam = (state) => {
    return (id) => {
        if (state.teams !== null) {
            return state.teams.find(team => team.id === id);
        } else {
            return null;
        }
    }
};

export const currentTeam = (state) => {
    return getTeam(state)(state.team);
};

export const currentBoard = (state) => {
    return state.board;
};

export const getQuestion = (state) => {
    return (cat_id, ques_id) => {
        let category = state.board.categories.find(cat => cat.id === cat_id);
        if (!category) {
            return null;
        }

        let question = category.questions.find(ques => ques.id === ques_id);
        return question;
    };
};

export const openQuestion = (state) => {
    return state.currentQuestion;
};

export const isQuestionOpen = (state) => {
    return state.currentQuestion !== null;
};

export const buzzerOpen = (state) => {
    return state.buzzer;
};

export const buzzedTeamId = (state) => {
    return state.buzzedTeam;
};

export const buzzedTeam = (state) => {
    return state.teams.find(t => t.id === state.buzzedTeam);
};

export const questionRevealed = (state) => {
    if (state.currentQuestion === null) {
        return false;
    }

    return state.currentQuestion.answer !== null;
};

export const isDailyDouble = (state) => {
    if (state.currentQuestion === null) {
        return false;
    }
    return state.currentQuestion.daily_double;
};

export const hasWager = (state) => {
    if (state.currentQuestion === null) {
        return false;
    }
    return !!state.currentQuestion.wager;
};