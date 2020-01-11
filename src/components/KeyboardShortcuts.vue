<template>
    <div class="overlay" v-if="open" role="alert">
        <div class="overlay-title">
            <h3>Keyboard Shortcuts</h3>
        </div>
        <div class="overlay-body">
            <div class="shortcut-section">
                <h4>General</h4>

                <table class="shortcut-table">
                    <tr>
                        <th><kbd class="shortcut">?</kbd></th>
                        <td>Show Help</td>
                    </tr>
                </table>
            </div>

            <div class="shortcut-section" v-if="loggedIn && isAdmin">
                <h4>Admin</h4>

                <table class="shortcut-table">
                    <tr>
                        <th>
                            <kbd class="shortcut">B</kbd>
                        </th>
                        <td>Toggle Buzzer State</td>
                    </tr>

                    <tr>
                        <th>
                            <kbd class="shortcut">1</kbd> - <kbd class="shortcut">{{ teamCount }}</kbd>
                        </th>
                        <td>Award Points to Team</td>
                    </tr>

                    <tr>
                        <th>
                            <kbd class="shortcut">Shift</kbd> + (<kbd class="shortcut">1</kbd> - <kbd class="shortcut">{{ teamCount }}</kbd>)
                        </th>
                        <td>Remove Points from Team</td>
                    </tr>

                    <tr>
                        <th>
                            <kbd class="shortcut">C</kbd>
                        </th>
                        <td>Close Cell</td>
                    </tr>

                    <tr>
                        <th>
                            <kbd class="shortcut">R</kbd>
                        </th>
                        <td>Reveal Question</td>
                    </tr>

                    <tr>
                        <th><kbd class="shortcut">S</kbd></th>
                        <td>Correct Score</td>
                    </tr>

                    <tr>
                        <th><kbd class="shortcut">N</kbd></th>
                        <td>Next Board / Start Game</td>
                    </tr>
                </table>
            </div>

            <div class="shortcut-section" v-if="loggedIn && !isAdmin">
                <h4>Team</h4>

                <table class="shortcut-table">
                    <tr>
                        <th><kbd class="shortcut">Any</kbd></th>
                        <td>Buzz In</td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
    import { mapGetters } from 'vuex';

    export default {
        name: 'keyboard-shortcuts',
        data() {
            return {
                open: false,
                listener: (event) => {
                    if (event.shiftKey && event.code === 'Slash') { this.open = !this.open; }
                },
            };
        },
        computed: {
            ...mapGetters(['isAdmin', 'loggedIn', 'teamCount']),
        },
        mounted() {
            addEventListener('keydown', this.listener);
        },
        destroyed() {
            removeEventListener('keydown', this.listener);
        },
    };
</script>

<style scoped>
    .overlay {
        left: 4%;
        width: 92%;
        top: 5%;
        z-index: 1002;
        color: #fff;
        position: fixed;
        text-align: center;
        font-family: arial, sans-serif;
        font-weight: bold;
        background: #222 none repeat scroll 0;
        overflow: hidden;
        opacity: .85;
        border-radius: 10px;
    }

    .overlay .overlay-body {
        padding: 1em;
    }

    .shortcut {
        font-family: "courier new", monospace;
        color: #dd0;
    }

    .shortcut-section li {
        list-style-type: none;
    }

    .shortcut-table {
        width: 100%;
    }

    .shortcut-table th {
        text-align: right;
    }

    .shortcut-table td {
        text-align: left;
        font-weight: normal;
    }
</style>
