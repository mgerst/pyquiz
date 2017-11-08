<template>
    <h1>{{ message }}</h1>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: 'waiting-room',
        computed: {
            ...mapGetters(['gameState']),
            message() {
                if (this.gameState === "waiting") {
                    return "Waiting for game to start";
                } else if (this.gameState === "finished") {
                    return "The game has finished";
                }
                return null;
            }
        }
    }
</script>
