<template>
    <div id="app" v-if="currentBoard">
        <div id="header" v-if="!isQuestionOpen">
            <h1 id="board-name">{{ name }}</h1>
        </div>

        <table id="game" v-if="!isQuestionOpen">
            <thead id="category-headers">
            <tr>
                <th v-for="cat in categories" :key="cat.id">{{ cat.name }}</th>
            </tr>
            </thead>
            <tbody id="questions">
            <tr v-for="question in height">
                <jeopardy-cell v-for="category in width" :key="String(category - 1) + '-' + String(width - 1)" :category="category" :question="question"></jeopardy-cell>
            </tr>
            </tbody>
        </table>

        <jeopardy-double v-if="isQuestionOpen"></jeopardy-double>
        <jeopardy-prompt v-if="isQuestionOpen"></jeopardy-prompt>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';
    import JeopardyCell from './JeopardyCell.vue';
    import JeopardyDouble from './Double.vue';
    import JeopardyPrompt from './Prompt.vue';

    export default {
        name: 'jeopardy-board',
        components: {
            JeopardyCell,
            JeopardyDouble,
            JeopardyPrompt,
        },
        computed: {
            ...mapGetters(['currentBoard', 'isQuestionOpen']),
            name() {
                if (this.currentBoard) {
                    return this.currentBoard.name;
                }
                return "Loading...";
            },
            categories() {
                if (this.currentBoard) {
                    return this.currentBoard.categories;
                }
                return [];
            },
            height() {
                if (this.currentBoard) {
                    return this.currentBoard.shape.height;
                }
                return 0;
            },
            width() {
                if (this.currentBoard) {
                    return this.currentBoard.shape.width;
                }
                return 0;
            }
        }
    }
</script>