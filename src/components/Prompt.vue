<template>
    <div id="prompt">
        <h1 id="answer">{{ openQuestion.clue }}</h1>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: 'jeopardy-prompt',
        computed: {
            ...mapGetters(['openQuestion']),
        }
    };
</script>