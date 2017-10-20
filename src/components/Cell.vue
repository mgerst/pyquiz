<template>
    <td @click="toggle">
        <span v-show="this.item.show">{{ value }}</span>
    </td>
</template>

<script>
    export default {
        name: 'jeopardy-cell',
        props: ['item'],
        computed: {
            value() {
                return this.item.value;
            },
        },
        methods: {
            toggle() {
                if (this.item.show) {
                    this.$store.commit('openQuestion', {value: this.item.value, category: this.item.category});
                }
            }
        }
    }
</script>