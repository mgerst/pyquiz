<template>
    <div id="app">
        <div id="header">
            <h1 id="board-name">{{ name }}</h1>
        </div>

        <table id="game" v-if="!isQuestionOpen">
            <thead id="category-headers">
            <tr>
                <th v-for="cat in categories">{{ cat.name }}</th>
            </tr>
            </thead>
            <tbody id="questions">
            <tr v-for="n in 5">
                <jeopardy-cell v-for="(cat, index) in categories" :item="cells[cat][n - 1]" :key="n + index"></jeopardy-cell>
            </tr>
            </tbody>
        </table>

        <jeopardy-double v-if="isQuestionOpen"></jeopardy-double>
        <jeopardy-prompt v-if="isQuestionOpen"></jeopardy-prompt>

        <div id="stats">
            <jeopardy-team v-for="team in teams" :team="team" :key="team.id"></jeopardy-team>
        </div>
    </div>
</template>

<script>
    import JeopardyCell from './Cell.vue';
    import JeopardyDouble from './Double.vue';
    import JeopardyPrompt from './Prompt.vue';
    import JeopardyTeam from './Team.vue';
    import {mapGetters} from 'vuex';

    export default {
        name: 'jeopardy-board',
        data: function() {
            return {
                name: "Loading Board",
            }
        },
        computed: {
            ...mapGetters(['categories', 'cells', 'teams', 'isQuestionOpen', 'boardName']),
        },
        components: {
            JeopardyCell,
            JeopardyDouble,
            JeopardyPrompt,
            JeopardyTeam,
        },
        watch: {
            boardName: function(val) {
                console.log("New Name", val);
            }
        }
    }
</script>