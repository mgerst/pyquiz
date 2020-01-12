<template>
    <div class="team-picker">
        <template v-if="!hideList">
            <h1>Team Picker</h1>

            <div class="player-choice" v-for="team in teamList" :key="team.id">
                <div class="player-select" @click="selectTeam(team.id)">
                    {{ team | teamName }}
                </div>
            </div>

            <div class="player-choice" v-if="showAdmin">
                <div class="player-select" @click="loginAdmin">
                    Admin
                </div>
            </div>

            <div class="player-choice" v-if="teamCount < maxTeams">
                <div class="player-select" @click="selectTeam(teamCount + 1)">
                    Create Team
                </div>
            </div>

            <div class="loading" v-if="teamList == null">
                Loading...
            </div>
            <div class="team-count" v-else>
                {{ teamCount }} of {{ maxTeams }} teams joined.
            </div>
        </template>

        <template v-if="currentTeam != null && currentTeam.taken">
            <form @submit.prevent="rejoin">
                <label for="key">Rejoin Key:</label>
                <input type="password" v-model="key"><br /><br />
                <button type="submit" @click="rejoin">Rejoin</button>
            </form>
        </template>

        <template v-if="currentTeam != null && !currentTeam.taken">
            <form @submit.prevent="join">
                <label for="name">Team Name:</label>
                <input type="text" id="name" v-model="name" />
                <label for="key">Key:</label>
                <input type="text" id="key" v-model="key" />
                <button type="submit" @click="join">Join</button>
            </form>
        </template>

        <template v-if="adminLogin">
            <form @submit.prevent="adminJoin">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="key" />
                <button type="submit" @click="adminJoin">Login</button>
            </form>
        </template>
    </div>
</template>

<script lang="ts">
    import Vue from 'vue';
    import Component from 'vue-class-component';
    import {
        Getter,
    } from 'vuex-class';
    import { Team } from '../store/types';

    @Component({
        name: 'team-picker',
    })
    export default class extends Vue {
        selectedTeam : number | null = null;
        adminLogin : boolean = false;
        hideList : boolean = false;
        key : string | null = null;
        name : string | null = null;

        @Getter teamList;
        @Getter getTeam;
        @Getter teamCount;
        @Getter maxTeams;

        get currentTeam() : Team | null {
            if (this.selectedTeam === null) { return null; }

            return this.getTeam(this.selectedTeam) || { id: this.selectedTeam, name: '', taken: false };
        }

        get showAdmin() : boolean {
            return window.jeopardy.admin;
        };

        selectTeam(id : number) {
            this.selectedTeam = id;
            this.hideList = true;
        }

        join() {
            this.$socket.client.emit('team.join', {
                id: this.selectedTeam,
                password: this.key,
                name: this.name,
            });
        }

        rejoin() {
            this.$socket.client.emit('team.join', {
                id: this.selectedTeam,
                password: this.key,
            });
        }

        adminJoin() {
            this.$socket.client.emit('admin.login', {
                password: this.key,
            });
        }

        loginAdmin() {
            this.adminLogin = true;
            this.hideList = true;
        }
    };
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