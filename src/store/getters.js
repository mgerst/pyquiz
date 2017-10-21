export const categories = (state) => {
    if (state.board === null) {
        return [];
    }
    return state.board.categories;
};

export const cells = (state) => {
    if (state.board === null) {
        return [];
    }
    return state.board.items;
};

export const teams = (state) => {
    return state.teams;
};

export const isQuestionOpen = (state) => {
    return state.question !== null;
};

export const openQuestion = (state) => {
    return state.question;
};

export const isDailyDouble = (state) => {
    return state.dailydouble.active;
};

export const hasWager = (state) => {
    return state.dailydouble.active && state.dailydouble.wager !== null;
};

export const isAdmin = (state) => {
    return state.admin;
};

export const buzzedTeam = (state) => {
    return state.buzzed;
};

export const currentTeam = (state) => {
    return state.currentTeam;
};

export const activeBoard = (state) => {
    return state.board !== null;
};

export const boardName = (state) => {
    if (state.board !== null) {
        return state.board.name;
    }
    return "";
};

export const isLoggedIn = (state) => {
    return state.logged_in;
};