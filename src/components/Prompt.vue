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

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: 'jeopardy-prompt',
        data() {
            return {
                listener: () => {
                    this.buzz();
                }
            }
        },
        computed: {
            ...mapGetters(['openQuestion', 'buzzerOpen', 'isAdmin', 'questionRevealed', 'isDailyDouble', 'hasWager', 'buzzedTeamId', 'currentBoard']),
            answer() {
                if (this.openQuestion) {
                    return this.openQuestion.answer;
                }
                return "";
            },
            value() {
                return this.openQuestion ? this.openQuestion.value : "";
            },
            isObserver() {
                return window.jeopardy.observer;
            },
            categoryName() {
                let category =  this.currentBoard.categories.find(cat => cat.id == this.openQuestion.category);
                return category === null ? "" : category.name;
            },
        },
        methods: {
            buzz() {
                if (this.buzzerOpen) {
                    this.$socket.emit('team.buzz');
                }
            },
        },
        mounted() {
            addEventListener('keypress', this.listener);
        },
        destroyed() {
            removeEventListener('keypress', this.listener);
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