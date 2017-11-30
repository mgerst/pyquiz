<template>
    <div class="admin-bar clearfix">
        <button @click="startGame" v-if="isWaiting">Start</button>
        <button v-if="isPlaying && !isQuestionOpen">Next Board</button>
        <button v-if="isPlaying && isQuestionOpen && !buzzerOpen && !questionRevealed" id="reopen" @click="openBuzzer">Open Buzzer</button>
        <button v-if="isPlaying && isQuestionOpen && !questionRevealed" id="correct-response" @click="reveal">Reveal</button>
        <button v-if="isPlaying && isQuestionOpen" id="back" @click="closeQuestion">Close</button>
        <button v-if="isPlaying && !correctingScore" id="correct-score" class="pull-right" @click="correctScore">Correct Score</button>

        <div class="score-correction pull-right clearfix" v-if="isPlaying && correctingScore">
            <input type="number" placeholder="Team #" v-model="team_number" id="team-number" class="pull-left" />
            <input type="number" placeholder="Score Change" v-model="score" id="score" class="pull-left" />
            <button class="pull-right" id="submit-score" @click="submitScore">Submit</button>
        </div>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: 'admin-bar',
        data() {
            return {
                correctingScore: false,
                team_number: null,
                score: null,
            }
        },
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
            },
            correctScore() {
                this.correctingScore = true;
            },
            submitScore() {
                this.correctingScore = false;

                if (this.team_number !== null && this.score !== null) {
                    this.$socket.emit('team.award', {
                        id: this.team_number,
                        amount: this.score,
                    });

                    this.team_number = null;
                    this.score = null;
                }
            }
        }
    }
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