<template>
  <div id="prompt" v-if="!isDailyDouble || hasWager">
    <h1 id="answer">{{ openQuestion.clue }}</h1>
    <button type="button" id="reopen" v-if="buzzedTeam" @click="reopen">Re-Open</button>
    <div id="buzzer-div" v-show="buzzedTeam === null">
      <button type="button" id="buzzer" @click="buzz" @keyup="buzz">Buzzer</button>
      <p>(or press the any key)</p>
    </div>
    <button type="button" @click="close">Close</button>
    <h1 id="question">{{ openQuestion.answer }}</h1>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex';

  export default {
    name: 'jeopardy-prompt',
    computed: {
      ...mapGetters(['openQuestion', 'hasWager', 'currentTeam', 'buzzedTeam', 'isAdmin', 'isDailyDouble'])
    },
    data() {
      return {
        listener: (evt) => {
          console.log(evt);
          this.buzz();
          this.clearListener();
        }
      }
    },
    methods: {
      close() {
        this.$store.commit('closeQuestion');
      },
      buzz() {
        this.$store.commit('setBuzzed');
      },
      reopen() {
        this.$store.commit('clearBuzzed');
      },
      clearListener() {
        removeEventListener('keypress', this.listener);
      }
    },
    mounted() {
      console.log("Mounted");
      addEventListener('keypress', this.listener);
    },
    destroyed() {
      this.clearListener();
    }
  }
</script>