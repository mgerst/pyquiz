<template>
    <div id="dailydouble" v-if="isDailyDouble && !hasWager">
        <h1>Daily Double!</h1>

        <div id="dailyadmin" v-if="isAdmin">
            <select v-model="team_number" placeholder="Team Number">
                <option :selected="team_number === null" disabled="true">Team Number</option>
                <option v-for="team in teamList" :key="team.id" :value="team.id" :selected="team_number == team.id ? true : false">
                    {{ team.id }} <span v-if="team.name"> - {{ team.name}}</span>
                </option>
            </select>
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
            ...mapGetters(['isAdmin', 'isDailyDouble', 'hasWager', 'teamList']),
        },
        methods: {
            makeWager() {
                this.$socket.client.emit('question.wager', {
                    team: this.team_number,
                    wager: this.wager,
                });
            }
        }
    };
</script>

<style scoped>
    #dailyadmin select, #dailyadmin input, #dailyadmin button {
        margin-top: .5em;
        padding: .5em;
    }
</style>