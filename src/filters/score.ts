export const score = (value : number) : string => {
    return value === 0 ? "-" : value.toString();
};

export const teamName = (team : any) : string => {
    if (!team.taken) {
        return `Team ${team.id}`;
    } else {
        return team.name;
    }
};