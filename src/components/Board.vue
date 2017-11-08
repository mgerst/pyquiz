<template>
    <div id="app" v-if="currentBoard">
        <div id="header">
            <h1 id="board-name">{{ name }}</h1>
        </div>

        <table id="game">
            <thead id="category-headers">
            <tr>
                <th v-for="cat in categories" :key="cat.id">{{ cat.name }}</th>
            </tr>
            </thead>
            <tbody id="questions">
            <tr v-for="category in height">
                <td v-for="question in width">{{ category }} - {{ question }}</td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: 'jeopardy-board',
        computed: {
            ...mapGetters(['currentBoard']),
            name() {
                if (this.currentBoard) {
                    return this.currentBoard.name;
                }
                return "Loading...";
            },
            categories() {
                if (this.currentBoard) {
                    return this.currentBoard.categories;
                }
                return [];
            },
            height() {
                if (this.currentBoard) {
                    return this.currentBoard.shape.height;
                }
                return 0;
            },
            width() {
                if (this.currentBoard) {
                    return this.currentBoard.shape.width;
                }
                return 0;
            }
        }
    }
</script>