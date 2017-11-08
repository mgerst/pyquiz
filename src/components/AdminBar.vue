<template>
    <div class="admin-bar">
        <button @click="startGame" v-if="isWaiting">Start</button>
        <button v-if="isPlaying">Next Board</button>
        <button v-if="isQuestionOpen && !buzzerOpen" id="reopen" @click="openBuzzer">Open Buzzer</button>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: 'admin-bar',
        computed: {
            ...mapGetters(['gameState', 'isQuestionOpen', 'buzzerOpen']),
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
            }
        }
    }
</script>