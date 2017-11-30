<template>
    <div id="app">
        <admin-bar v-if="isAdmin"></admin-bar>
        <team-picker v-if="!loggedIn && !isObserver"></team-picker>
        <waiting-room v-if="loggedIn && !isAdmin"></waiting-room>

        <jeopardy-board v-if="gameState === 'playing' && loggedIn"></jeopardy-board>

        <div id="stats">
            <jeopardy-team v-for="team in teamList" :key="team.id" :team="team"></jeopardy-team>
        </div>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';
    import AdminBar from './components/AdminBar.vue';
    import Board from './components/Board.vue';
    import TeamPicker from './components/TeamPicker.vue';
    import TeamScore from './components/Team.vue';
    import WaitingRoom from './components/WaitingRoom.vue';

    export default {
        name: 'app',
        data() {
            return {}
        },
        methods: {
        },
        components: {
            AdminBar,
            'jeopardy-board': Board,
            TeamPicker,
            'jeopardy-team': TeamScore,
            WaitingRoom,
        },
        computed: {
            ...mapGetters(['loggedIn', 'isAdmin', 'teamList', 'gameState']),
            isObserver() {
                return window.jeopardy.observer;
            }
        },
    }
</script>

<style>
    body {
        background-color: #2a3698;
        height: 100%;
        font-family: Verdana, Arial, Helvetica, sans-serif;
        padding-bottom: 100px;
        padding-left: 40px;
        padding-right: 40px;
    }

    label {
        display: block;
        font-size: 16px;
    }

    input, textarea, select {
        display: block;
        font-family: Verdana, Arial, Helvetica, sans-serif;
        margin: auto;
    }

    #board-name {
        color: white;
    }

    textarea {
        padding: 5px;
    }

    .clear {
        clear: both;
    }

    .hide {
        display: none;
    }

    #game {
        width: 100%;
        background-color: #000000;
        padding: 0;
        margin: 0;
        margin: auto;
        font-size: 16px;
    }

    #game textarea {
        width: 90%;
        height: 30px;
        font-size: 18px;
        line-height: 22px;
    }

    #game h3 {
        color: #ffff5f;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    }

    #game tbody td, #game thead th {
        vertical-align: middle;
        background-color: #2a3698;
        padding: 5px;
        text-align: center;
        width: 16%;
        color: #ffff5f;
        height: 60px;
        font-size: 20px;

    }

    #game tbody td {
        cursor: pointer;
        height: 100px;
        border: 3px solid #2a3698;
    }

    #game tbody td:hover {
        border: 3px solid #ffff5f;
    }

    #game tbody td.dirty h3 {
        color: #2a3698;
    }

    #game tfoot td {
        text-align: center;
        background-color: #2a3698;
    }

    h1 {
        color: white;
    }

    #prompt, #dailydouble {
        height: 100%;
        width: 100%;
        background-color: #2a3698;
        color: #FFFFFF;
        text-align: center;
        margin-top: 60px;
    }

    #prompt a:link, #prompt a:visited, #prompt a:hover {
        color: #fff;
        font-size: 18px;
        text-decoration: underline;
    }

    #prompt a:hover {
        text-decoration: none;
    }

    #answer {
        padding-left: 5%;
        padding-right: 5%;
    }

    #question {
        padding-left: 5%;
        padding-right: 5%;
    }

    button {
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 32px;
        background-color: cornflowerblue;
    }

    #buzzer, #reopen {
        background-color: red;
    }

    #correct-response {
        background-color: green;
    }

    #correct-score {
        background-color: goldenrod;
    }

    #continue {
        background-color: cornflowerblue;
    }

    #board-name {
        float: left;
    }

    #next_board {
        background-color: cornflowerblue;
        padding: 10px 28px;
        display: inline;
        /*float: right;*/
        margin-left: 10px;
    }

    #stats {
        position: fixed;
        bottom: 0;
        background-color: #ffffff;
        width: 100%;
        text-align: center;
        height: 110px;
        display: flex;
        left: 0;
    }

    #stats .team {
        flex-grow: 1;
        margin: 10px;
    }

    .buzzedin {
        border: 1px solid green;
    }

    .team h5, .team span {
        pointer-events: none;
    }

    a {
        color: white;
    }

    .pull-right {
        float: right;
    }

    .pull-left {
        float: left;
    }

    .clearfix {
        overflow: auto;
    }
</style>