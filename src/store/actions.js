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
    console.log("Switching board", data);
};

export const socket_boardCurrent = (context, data) => {
    console.log("Current board", data);
};