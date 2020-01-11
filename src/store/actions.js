export const socket_youAre = (context, message) => {
    context.commit('setIdentity', message);
};

export const socket_gameState = (context, {state}) => {
    context.commit('setState', state);
};

export const socket_teamList = (context, {teams, max_teams}) => {
    context.commit('setTeams', { teams, max_teams });
};

export const socket_teamJoined = (context, data) => {
    context.commit('teamJoin', data);
};

export const socket_boardSwitch = (context, data) => {
    // TODO: Actually handle board types. This event doesn't currently do anything
    console.log("Switching board", data);
};

export const socket_boardCurrent = (context, data) => {
    context.commit('boardCurrent', data);
};

export const socket_questionOpen = (context, data) => {
    context.commit('questionOpen', data);
};

export const socket_buzzerOpen = (context) => {
    context.commit('buzzerOpen');
};

export const socket_buzzerClose = (context, {team}) => {
    context.commit('buzzerClose', team);
};

export const socket_teamScore = (context, data) => {
    console.log("update team score", data);
    context.commit('updateScore', data);
};

export const socket_questionReveal = (context, data) => {
    context.commit('questionReveal', data);
};

export const socket_questionClose = (context) => {
    context.commit('questionClose');
};

export const socket_questionWager = (context) => {
    context.commit('questionWager');
};

export const socket_error = (context, data) => {
    console.error("Got error from server:", data);
};