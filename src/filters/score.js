export const score = (value) => {
    return value === 0 ? "-" : value;
};

export const teamName = (team) => {
    if (team.taken === false) {
        return `Team ${team.id}`;
    } else {
        return team.name;
    }
};