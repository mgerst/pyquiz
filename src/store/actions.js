export const socket_youAre = (context, message) => {
    context.commit('setIdentity', message);
};

export const socket_teamList = (context, data) => {
    context.commit('setTeamList', {teams: data});
};

export const socket_boardCurrent = (context, data) => {
    console.log("board.current", data);

    const categories = Object.keys(data.categories).map(cat => {
        let obj = data.categories[cat];
        return {id: obj.id, name: obj.name};
    });

    const items = Object.keys(data.categories).reduce((obj, x) => {
        let category = data.categories[x];
        obj[category.id] = category.questions;
        return obj;
    }, {});

    console.log("board.current", categories, items);
    context.commit('setBoard', {categories, items, name: data.name});
};