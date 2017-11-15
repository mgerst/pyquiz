<template>
    <div id="dailydouble" v-if="isDailyDouble && !hasWager">
        <h1>Daily Double!</h1>

        <div id="dailyadmin" v-if="isAdmin">
            <input type="text" v-model="team_number" placeholder="Team Number" />
            <input type="text" v-model="wager" placeholder="Wager" />
            <button type="button" id="dailysubmit" @click="makeWager">Start</button>
        </div>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: 'jeopardy-double',
        data() {
            return {
                team_number: null,
                wager: null,
            }
        },
        computed: {
            ...mapGetters(['isAdmin', 'isDailyDouble', 'hasWager']),
        },
        methods: {
            makeWager() {
                this.$socket.emit('question.wager', {
                    team: this.team_number,
                    wager: this.wager,
                });
            }
        }
    };
</script>