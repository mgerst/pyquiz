<template>
    <div id="app">What? {{ name }}</div>
</template>

<script>
    export default {
        name: 'app',
        data() {
            return {
                name: 'Finally!'
            }
        }
    }
</script>