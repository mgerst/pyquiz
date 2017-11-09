<template>
    <div class="team" :class="{buzzedin: buzzed}" @click.prevent="award" @contextmenu.prevent="detract">
        <h5 class="name">{{ identifier }}</h5>
        <span class="score">{{ team.score | score }}</span>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: 'jeopardy-team',
        props: ['team'],
        computed: {
            ...mapGetters(['buzzedTeamId', 'openQuestion', 'isAdmin', 'isDailyDouble']),
            buzzed() {
                return this.team.id === this.buzzedTeamId;
            },
            identifier() {
                return this.team.name === null ? `Team ${this.team.id}` : this.team.name;
            },
        },
        methods: {
            award() {
                let amount = this.isDailyDouble ? 1 : this.openQuestion.value;
                if (this.buzzed && this.isAdmin) {
                    this.$socket.emit('team.award', {
                        id: this.team.id,
                        amount: amount,
                    });
                }
            },
            detract() {
                // The 1 will get inverted server-side
                let amount = this.isDailyDouble ? 1 : this.openQuestion.value;
                if (this.buzzed && this.isAdmin) {
                    this.$socket.emit('team.detract', {
                        id: this.team.id,
                        amount: amount,
                    });
                }
            }
        }
    }
</script>