<template>
    <div class="team" :class="{buzzedin: buzzed}" @click.prevent="award" @contextmenu.prevent="detract">
        <h5 class="name">{{ identifier }}</h5>
        <span class="score">{{ team.score | score }}</span>
    </div>
</template>

<script lang="ts">
    import Vue from 'vue';
    import { Component, Prop } from 'vue-property-decorator';
    import {
        Getter,
    } from 'vuex-class';
    import { Team } from '../store/types';

    @Component({
        name: 'jeopardy-team',
    })
    export default class extends Vue {
        @Prop() team! : Team;

        @Getter buzzedTeamId;
        @Getter openQuestion;
        @Getter isAdmin;
        @Getter isDailyDouble;

        get buzzed() : boolean {
            return this.team.id === this.buzzedTeamId;
        }

        get identifier() : string {
            return this.team.name === null ? `Team ${this.team.id}` : this.team.name;
        }

        award() {
            if (!this.openQuestion) { return; }

            const amount = this.isDailyDouble ? 1 : this.openQuestion.value;
            if (this.buzzed && this.isAdmin) {
                this.$socket.client.emit('team.award', {
                    id: this.team.id,
                    amount: amount,
                });
            }
        }

        detract() {
            if (!this.openQuestion) { return; }

            // The 1 will get inverted server-side
            const amount = this.isDailyDouble ? 1 : this.openQuestion.value;
            if (this.buzzed && this.isAdmin) {
                this.$socket.client.emit('team.detract', {
                    id: this.team.id,
                    amount: amount,
                });
            }
        }

        handleKeyPress(event) {
            if (event.shiftKey && event.code === `Digit${this.team.id}`) { this.detract(); }
            else if (event.code === `Digit${this.team.id}`) { this.award(); }
        }

        mounted() {
            addEventListener('keydown', this.handleKeyPress);
        }

        destroyed() {
            removeEventListener('keydown', this.handleKeyPress);
        }
    };
</script>