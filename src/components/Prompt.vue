<template>
    <div id="prompt">
        <h1 id="answer">{{ openQuestion.clue }}</h1>

        <div id="buzzer-div" v-show="buzzerOpen && !isAdmin">
            <button type="button" id="buzzer" @click="buzz" @keyup="buzz">Buzzer</button>
            <p>(or press the any key)</p>
        </div>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: 'jeopardy-prompt',
        computed: {
            ...mapGetters(['openQuestion', 'buzzerOpen', 'isAdmin']),
        },
        methods: {
            buzz() {

            }
        }
    };
</script>