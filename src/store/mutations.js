export const setIdentity = (state, {admin, team, logged_in}) => {
    state.admin = admin;
    state.team = team;
    state.logged_in = logged_in;
};

export const setState = (state, gameState) => {
    state.state = gameState;
};

export const setTeams = (state, {teams, max_teams}) => {
    state.teams = teams;
    state.max_teams = max_teams;
};

export const teamJoin = (state, {team, name}) => {
    let found_team = state.teams.find(t => team === t.id);
    found_team.taken = true;
    found_team.name = name;
};

export const boardCurrent = (state, data) => {
    state.board = data;
};

export const questionOpen = (state, {question, category, clue, value, daily_double, type}) => {
    state.currentQuestion = {
        id: question,
        category: category,
        clue: clue,
        value: value,
        answer: null,
        daily_double: daily_double,
        wager: null,
        type: type,
    };
};

export const questionReveal = (state, {answer}) => {
    state.currentQuestion.answer = answer;
};

export const buzzerOpen = (state) => {
    state.buzzer = true;
    state.buzzedTeam = null;
};

export const buzzerClose = (state, team) => {
    state.buzzer = false;
    state.buzzedTeam = team;
};

export const updateScore = (state, {team, score}) => {
    state.teams.find(t => t.id === team).score = score;
    buzzerClose(state, null);
};

export const questionClose = (state) => {
    let cat_id = state.currentQuestion.category;
    let q_id = state.currentQuestion.id;
    state.currentQuestion = null;
    buzzerClose(state, null);

    let category = state.board.categories.find(cat => cat.id === cat_id);
    let question = category.questions.find(ques => ques.id === q_id);
    console.log(cat_id, q_id, category, question);
    if (question) {
        question.visible = false;
    }
};

export const questionWager = (state) => {
    if (!state.admin || !state.currentQuestion.wager) {
        state.currentQuestion.wager = true;
    }
};