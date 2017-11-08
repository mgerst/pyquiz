<template>
    <td @click="open">
        <span v-show="current.visible">{{ value }}</span>
    </td>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: 'jeopardy-cell',
        props: ['category', 'question'],
        computed: {
            ...mapGetters(['getQuestion', 'isAdmin']),
            current() {
                return this.getQuestion(this.category, this.question);
            },
            value() {
                if (this.current !== null) {
                    return this.current.value;
                }
                return null;
            },
        },
        methods: {
            open() {
                if (this.isAdmin) {
                    this.$socket.emit('question.open', {
                        question: this.question,
                        category: this.category,
                    })
                } else {
                    console.log("Can't open question as non-admin");
                }
            }
        }
    }
</script>