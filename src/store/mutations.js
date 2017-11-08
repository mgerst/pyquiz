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