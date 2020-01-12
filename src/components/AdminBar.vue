<template>
    <div class="admin-bar clearfix">
        <button @click="startGame" v-if="isWaiting">Start</button>
        <template v-if="isPlaying">
            <button v-if="!isQuestionOpen">Next Board</button>

            <template v-if="isQuestionOpen">
                <button v-if="!buzzerOpen && !questionRevealed" id="reopen" @click="openBuzzer">Open Buzzer</button>
                <button v-if="!questionRevealed" id="correct-response" @click="reveal">Reveal</button>
                <button id="back" @click="closeQuestion">Close</button>
            </template>

            <button v-if="!correctingScore" id="correct-score" class="pull-right" @click="correctScore">Correct Score</button>
        </template>

        <div class="score-correction pull-right clearfix" v-if="isPlaying && correctingScore">
            <input type="number" placeholder="Team #" v-model="team_number" id="team-number" class="pull-left" />
            <input type="number" placeholder="Score Change" v-model="score" id="score" class="pull-left" />
            <button class="pull-right" id="submit-score" @click="submitScore">Submit</button>
        </div>
    </div>
</template>

<script lang="ts">
    import Vue from 'vue';
    import Component from 'vue-class-component';
    import {
        Getter,
    } from 'vuex-class';

    @Component({
        name: 'admin-bar',
    })
    export default class extends Vue {
        correctingScore : boolean = false;
        team_number : number | null = null;
        score : number | null = null;

        @Getter gameState;
        @Getter isQuestionOpen;
        @Getter buzzerOpen;
        @Getter questionRevealed;

        get isWaiting() : boolean {
            return this.gameState === 'waiting';
        }

        get isPlaying() : boolean {
            return this.gameState === 'playing';
        }

        get isFinished() : boolean {
            return this.gameState === 'finished';
        }

        startGame() {
            this.$socket.client.emit('game.start');
        }

        openBuzzer() {
            this.$socket.client.emit('buzzer.open');
        }

        reveal() {
            this.$socket.client.emit('question.reveal');
        }

        closeQuestion() {
            this.$socket.client.emit('question.close');
        }

        correctScore() {
            this.correctingScore = true;
        }

        submitScore() {
            this.correctingScore = false;

            if (this.team_number !== null && this.score !== null) {
                this.$socket.client.emit('team.award', {
                    id: this.team_number,
                    amount: this.score,
                });

                this.team_number = null;
                this.score = null;
            }
        }

        handleKeyPress(event) {
            if (this.isWaiting && event.code === 'KeyN') {
                this.startGame();
            } else if (this.isPlaying) {
                if (this.isQuestionOpen) {
                    if (!this.buzzerOpen && !this.questionRevealed && event.code === 'KeyB') {
                        this.openBuzzer();
                    } else if (!this.questionRevealed && event.code === 'KeyR') {
                        this.reveal();
                    } else if (event.code === 'KeyC') {
                        this.closeQuestion();
                    }
                } else if (event.code === 'KeyN') {
                    // TODO: handle next board
                } else if (!this.correctingScore && event.code === 'KeyS') {
                    this.correctScore();
                }
            }
        }

        mounted() {
            addEventListener('keydown', this.handleKeyPress);
        }

        destroyed() {
            addEventListener('keydown', this.handleKeyPress);
        }
    };
</script>

<style scoped>
    #team-number {
        margin: 5px;
    }

    #score {
        margin: 5px;
    }

    #submit-score {
        margin: 5px;
    }
</style>