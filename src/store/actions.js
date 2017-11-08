export const socket_youAre = (context, message) => {
    context.commit('setIdentity', message);
};

export const socket_gameState = (context, {state}) => {
    context.commit('setState', state);
};

export const socket_teamList = (context, {teams}) => {
    context.commit('setTeams', teams);
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