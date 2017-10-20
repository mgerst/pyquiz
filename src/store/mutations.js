export const openQuestion = (state, {value, category}) => {
    if (state.question !== null) {
        console.error("Opened question when another question is already open!");
    }

    let item = state.board.items[category].find(item => item.value === value);
    item.show = false;

    state.question = item;
    state.dailydouble.active = item.dailydouble || false;
};

export const closeQuestion = (state) => {
    state.question = null;
    if (state.dailydouble.active) {
        state.dailydouble = {
            active: false,
            teamId: null,
            wager: null,
        }
    }
    state.buzzed = null;
};

export const modifyScore = (state, {teamId, value}) => {
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
};

export const setAdmin = (state, {value}) => {
    state.admin = value;
};

export const setWager = (state, {teamId, wager}) => {
    state.dailydouble.wager = wager;
    state.dailydouble.teamId = teamId;
};

export const setBuzzed = (state) => {
    if (state.buzzed !== null) {
        return;
    }

    state.buzzed = state.currentTeam;
};

export const clearBuzzed = (state) => {
    state.buzzed = null;
};