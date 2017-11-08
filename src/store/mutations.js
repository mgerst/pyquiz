export const setIdentity = (state, {admin, team, logged_in}) => {
    state.admin = admin;
    state.team = team;
    state.logged_in = logged_in;
};

export const setState = (state, gameState) => {
    state.state = gameState;
};

export const setTeams = (state, teams) => {
    state.teams = teams;
};

export const teamJoin = (state, {team, name}) => {
    let found_team = state.teams.find(t => team === t.id)
    found_team.taken = true;
    found_team.name = name;
};

export const boardCurrent = (state, data) => {
    state.board = data;
};

export const questionOpen = (state, {question, category, clue, value}) => {
    state.currentQuestion = {
        id: question,
        category: category,
        clue: clue,
        value: value,
    };
};

export const buzzerOpen = (state) => {
    state.buzzer = true;
    state.buzzedTeam = null;
};

export const buzzerClose = (state, team) => {
    state.buzzer = false;
    state.buzzedTeam = team;
};