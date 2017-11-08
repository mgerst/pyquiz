<template>
    <div class="team-picker">
        <template v-if="selectedTeam == null">
            <h1>Team Picker</h1>

            <div class="player-choice" v-for="team in teamList" :key="team.id">
                <div class="player-select" @click="selectTeam(team.id)">
                    <template v-if="team.taken">{{ team.name }}</template>
                    <template v-else>Team {{ team.id }}</template>
                </div>
            </div>

            <div class="loading" v-if="teamList == null">
                Loading...
            </div>
        </template>

        <template v-if="currentTeam != null && currentTeam.taken">
            <form @submit.prevent="rejoin">
                <label for="key">Rejoin Key:</label>
                <input type="text" v-model="key"><br /><br />
                <button type="button" @click="rejoin">Rejoin</button>
            </form>
        </template>

        <template v-if="currentTeam != null && !currentTeam.taken">
            <form @submit.prevent="join">
                <label for="name">Team Name:</label>
                <input type="text" v-model="name" />
                <label for="key">Key:</label>
                <input type="text" v-model="key" />
                <button type="button" @click="join">Join</button>
            </form>
        </template>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: "team-picker",
        data() {
            return {
                selectedTeam: null,
                key: null,
                name: null,
            }
        },
        computed: {
            ...mapGetters(['teamList', 'getTeam']),
            currentTeam() {
                return this.getTeam(this.selectedTeam);
            }
        },
        methods: {
            selectTeam(id) {
                this.selectedTeam = id;
            },
            join() {
                this.$socket.emit('team.join', {
                    id: this.selectedTeam,
                    password: this.key,
                    name: this.name,
                });
            },
            rejoin() {
                this.$socket.emit('team.join', {
                    id: this.selectedTeam,
                    password: this.key,
                });
            },
        }
    }
</script>

<style>
    .team-picker {
        text-align: center;
    }

    .player-select {
        color: white;
        text-decoration: underline;
        font-size: 14pt;
        margin: 6px;
    }
</style>