<template>
    <div class="admin-bar">
        <button @click="startGame" v-if="isWaiting">Start</button>
        <button v-if="isPlaying">Next Board</button>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: 'admin-bar',
        computed: {
            ...mapGetters(['gameState']),
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
            }
        }
    }
</script>