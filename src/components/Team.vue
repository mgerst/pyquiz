<template>
    <div class="team">
        <h5 class="name">{{ identifier }}</h5>
        <span class="score">{{ team.score | score }}</span>
    </div>
</template>

<script>
    export default {
        name: 'jeopardy-team',
        props: ['team'],
        computed: {
            identifier() {
                return this.team.name === null ? `Team ${this.team.id}` : this.team.name;
            }
        }
    }
</script>