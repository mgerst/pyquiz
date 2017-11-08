<template>
    <div class="admin-bar">
        <button @click="startGame" v-if="isWaiting">Start</button>
        <button v-if="isPlaying && !isQuestionOpen">Next Board</button>
        <button v-if="isPlaying && isQuestionOpen && !buzzerOpen && !questionRevealed" id="reopen" @click="openBuzzer">Open Buzzer</button>
        <button v-if="isPlaying && isQuestionOpen && !questionRevealed" id="correct-response" @click="reveal">Reveal</button>
        <button v-if="isPlaying && isQuestionOpen" id="back" @click="closeQuestion">Close</button>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: 'admin-bar',
        computed: {
            ...mapGetters(['gameState', 'isQuestionOpen', 'buzzerOpen', 'questionRevealed']),
            isWaiting() {
                return this.gameState === 'waiting';
            },
            isPlaying() {
                return this.gameState === 'playing';
            },
            isFinished() {
                return this.gameState === 'finished';
            },
        },
        methods: {
            startGame() {
                this.$socket.emit('game.start');
            },
            openBuzzer() {
                this.$socket.emit('buzzer.open');
            },
            reveal() {
                this.$socket.emit('question.reveal');
            },
            closeQuestion() {
                this.$socket.emit('question.close');
            }
        }
    }
</script>