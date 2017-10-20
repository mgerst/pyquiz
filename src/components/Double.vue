<template>
  <div id="dailydouble" v-if="isDailyDouble && !hasWager">
    <h1>Daily Double!</h1>

    <div id="dailyadmin" v-if="isAdmin">
      <input type="text" v-model="team_number" placeholder="Team Number"/>
      <input type="text" v-model="wager" placeholder="Wager"/>
      <button type="button" id="dailysubmit" @click="submitWager">Start</button>
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
      ...mapGetters(['isDailyDouble', 'hasWager', 'isAdmin']),
    },
    methods: {
      submitWager() {
        this.$store.commit('setWager', {teamId: parseInt(this.team_number), wager: parseInt(this.wager)});
      }
    }
  };
</script>