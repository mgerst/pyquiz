<template>
    <td @click="open">
        <span v-show="current.visible">{{ value }}</span>
    </td>
</template>

<script lang="ts">
    import Vue from 'vue';
    import { Component, Prop } from 'vue-property-decorator';
    import {
        Getter,
    } from 'vuex-class';
    import { Question } from '../store/types';

    @Component({
        name: 'jeopardy-cell',
    })
    export default class extends Vue {
        @Prop({ type: Number }) readonly category! : number;
        @Prop({ type: Number }) readonly question! : number;

        @Getter getQuestion;
        @Getter isAdmin;

        get current() : Question | null {
            return this.getQuestion(this.category, this.question);
        }

        get value() : number | null {
            return this.current !== null ? this.current.value : null;
        }

        open() {
            if (this.isAdmin) {
                this.$socket.client.emit('question.open', {
                    question: this.question,
                    category: this.category,
                })
            } else {
                console.log("Can't open question as non-admin");
            }
        }
    };
</script>