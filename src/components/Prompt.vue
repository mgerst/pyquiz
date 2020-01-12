<template>
    <div id="prompt" v-if="!isDailyDouble || hasWager">
        <div class="clearfix">
            <h1 id="category" class="pull-left">{{ categoryName }} ({{ value }})</h1>
        </div>
        <h1 id="answer" v-if="openQuestion.type === 'text'">{{ openQuestion.clue }}</h1>
        <div id="answer" v-if="openQuestion.type === 'image'">
            <img :src="openQuestion.clue"/>
        </div>

        <div id="buzzer-div" v-show="buzzerOpen && !isAdmin && !isObserver">
            <button type="button" id="buzzer" @click="buzz" @keyup="buzz">Buzzer</button>
            <p>(or press the any key)</p>
        </div>

        <h1 id="team_buzzed" v-if="buzzedTeamId">Team {{ buzzedTeamId }} buzzed in!</h1>
        <h1 id="question" v-if="questionRevealed">{{ answer }}</h1>
    </div>
</template>

<script lang="ts">
    import Vue from 'vue';
    import Component from 'vue-class-component';
    import {
        Getter,
    } from 'vuex-class';
    import {mapGetters} from 'vuex';

    @Component({
        name: 'jeopardy-prompt',
    })
    export default class extends Vue {
        @Getter openQuestion;
        @Getter buzzerOpen;
        @Getter isAdmin;
        @Getter questionRevealed;
        @Getter isDailyDouble;
        @Getter hasWager;
        @Getter buzzedTeamId;
        @Getter currentBoard;

        get answer() : string {
            return this.openQuestion ? this.openQuestion.answer : "";
        }

        get value() : string {
            return this.openQuestion ? this.openQuestion.value : "";
        }

        get isObserver() : boolean {
            return window.jeopardy.observer;
        }

        get categoryName() : string {
            const category = this.currentBoard.categories.find(cat => cat.id == this.openQuestion.category);
            return category === null ? "" : category.name;
        }

        buzz() {
            if (this.buzzerOpen) { this.$socket.client.emit('team.buzz'); }
        }

        handleKeyDown() {
            this.buzz();
        }

        mounted() : void {
            addEventListener('keydown', this.handleKeyDown);
        }

        destroyed() : void {
            removeEventListener('keydown', this.handleKeyDown);
        }
    };
</script>

<style scoped>
    .pull-left {
        float: left;
    }

    .clearfix {
        overflow: auto;
    }
</style>