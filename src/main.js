import Vue from 'vue'
import VueSocketIOExt from 'vue-socket.io-extended';
import io from 'socket.io-client';
import App from './App.vue'
import {score, teamName} from './filters/score'
import store from './store'

const socket = io(`${location.protocol}//${document.domain}:${location.port}`);

Vue.use(VueSocketIOExt, socket, {
    store,
    actionPrefix: 'socket_',
    eventToActionTransformer(name) {
        console.debug('action transform', name);
        return VueSocketIOExt.defaults.eventToActionTransformer(name);
    },
});
// Vue.use(VueSocketIOExt, socket);

Vue.config.productionTip = false;
Vue.filter('score', score);
Vue.filter('teamName', teamName);

new Vue({
    el: "#app",
    store,
    render: h => h(App),
    components: {App},
    sockets: {
        connect() {
            this.$socket.client.emit('whoami');
        },
    },
});