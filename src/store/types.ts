export interface Team {
    id : number;
    name : string | null;
    score : number;
    taken : boolean;
}

export interface Question {
    id : number
    value : number
    answer : string
    question : string
    category : number
    daily_double : boolean
    visible : boolean
}

export enum QuestionType {
    Text = 'text',
    Image = 'image',
}

export interface CurrentQuestion {
    id : number
    category : number
    clue : string
    value : number
    answer? : string | null
    daily_double : boolean
    wager? : boolean | number | null
    type : QuestionType
}

export interface Category {
    id : number
    name : string
    questions : Question[]
}

export interface Shape {
    width : number
    height : number
}

export interface Board {
    id : number;
    name : string;
    shape : Shape;
    categories : Category[]
}

export enum State {
    Unknown = 'unknown',
    Playing = 'playing',
    Finished = 'finished',
}

export interface RootState {
    state : State;
    admin : boolean;
    team : number | null;
    logged_in : boolean;
    teams : Team[];
    max_teams : number;
    board : Board | null;
    currentQuestion : CurrentQuestion | null;
    buzzer : boolean;
    buzzedTeam : number | null;
}