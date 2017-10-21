<template>
  <div class="team" @click="award" @contextmenu="detract" :class="{buzzedin: buzzed}">
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
      ...mapGetters(['isQuestionOpen', 'openQuestion', 'buzzedTeam']),
      buzzed() {
        return this.team.id === this.buzzedTeam;
      },
      identifier() {
        return this.team.name === null ? `Team ${this.team.id}` : this.team.name;
      },
    },
    methods: {
      award(evt) {
        if (this.buzzed) {
          this.$store.commit('modifyScore', {teamId: this.team.id, value: +1});
        }
      },
      detract(evt) {
        evt.preventDefault();

        if (this.buzzed) {
          this.$store.commit('modifyScore', {teamId: this.team.id, value: -1});
        }
      },
    }
  }
</script>
