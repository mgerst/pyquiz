<template>
    <div class="waiting-room">
        <h1>{{ message }}</h1>
        <h2>Team: {{ team }}</h2>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: 'waiting-room',
        computed: {
            ...mapGetters(['gameState', 'currentTeam']),
            team() {
                const team = this.currentTeam;
                return team.name || team.id;
            },
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

<style scoped>
    .waiting-room {
        color: white;
    }
</style>