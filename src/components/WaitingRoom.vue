<template>
    <div class="waiting-room">
        <h1>{{ message }}</h1>
        <h2 v-if="!observer">Team: {{ team }}</h2>
    </div>
</template>

<script lang="ts">
    import Vue from 'vue';
    import Component from 'vue-class-component';
    import {
        Getter,
    } from 'vuex-class';

    @Component({
        name: 'waiting-room',
    })
    export default class extends Vue {
        @Getter gameState;
        @Getter currentTeam;

        get team() : string | number {
            const team = this.currentTeam;
            return team.name || team.id;
        }

        get message() : string | null {
            if (this.gameState === "waiting") {
                return "Waiting for game to start";
            } else if (this.gameState === "finished") {
                return "The game has finished";
            }
            return null;
        }

        get observer() : boolean {
            return !!window.jeopardy.observer;
        }
    };
</script>

<style scoped>
    .waiting-room {
        color: white;
    }
</style>