<template>
    <div id="prompt">
        <h1 id="answer">{{ openQuestion.clue }}</h1>

        <div id="buzzer-div" v-show="buzzerOpen && !isAdmin && !isObserver">
            <button type="button" id="buzzer" @click="buzz" @keyup="buzz">Buzzer</button>
            <p>(or press the any key)</p>
        </div>

        <h1 id="question" v-if="questionRevealed">{{ answer }}</h1>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: 'jeopardy-prompt',
        computed: {
            ...mapGetters(['openQuestion', 'buzzerOpen', 'isAdmin', 'questionRevealed']),
            answer() {
                if (this.openQuestion) {
                    return this.openQuestion.answer;
                }
                return "";
            },
            isObserver() {
                return window.jeopardy.observer;
            }
        },
        methods: {
            buzz() {
                this.$socket.emit('team.buzz');
            },
        }
    };
</script>