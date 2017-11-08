<template>
    <td>
        <span v-show="current.visible">{{ value }}</span>
    </td>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: 'jeopardy-cell',
        props: ['category', 'question'],
        computed: {
            ...mapGetters(['getQuestion']),
            current() {
                return this.getQuestion(this.category, this.question);
            },
            value() {
                if (this.current !== null) {
                    return this.current.value;
                }
                return null;
            },
        }
    }
</script>