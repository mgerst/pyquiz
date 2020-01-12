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

<script lang="ts">
    import Vue from 'vue';
    import Component from 'vue-class-component';
    import {
        Getter,
    } from 'vuex-class';
    import JeopardyCell from './JeopardyCell.vue';
    import JeopardyDouble from './Double.vue';
    import JeopardyPrompt from './Prompt.vue';

    @Component({
        name: 'jeopardy-board',
        components: {
            JeopardyCell,
            JeopardyDouble,
            JeopardyPrompt,
        }
    })
    export default class extends Vue {
        @Getter currentBoard;
        @Getter isQuestionOpen;

        get name() : string {
            return this.currentBoard ? this.currentBoard.name : 'Loading...';
        }

        get categories() : Array<Object> {
            return this.currentBoard ? this.currentBoard.categories : [];
        }

        get height() : number {
            return this.currentBoard ? this.currentBoard.shape.height : 0;
        }

        get width() : number {
            return this.currentBoard ? this.currentBoard.shape.width : 0;
        }
    };
</script>