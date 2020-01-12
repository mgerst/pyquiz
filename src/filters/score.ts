import { Team } from '../store/types';

export const score = (value : number) : string => {
    return value === 0 ? "-" : value.toString();
};

export const teamName = (team : Team) : string => {
    if (!team.taken || !team.name) {
        return `Team ${team.id}`;
    } else {
        return team.name;
    }
};