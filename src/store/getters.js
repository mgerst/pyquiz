export const gameState = (state) => {
    return state.state;
};

export const loggedIn = (state) => {
    return state.logged_in;
};

export const teamList = (state) => {
    return state.teams;
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