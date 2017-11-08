import Vue from 'vue'
import VueSocketio from 'vue-socket.io';
import App from './App.vue'
import {score, teamName} from './filters/score'
import store from './store'

Vue.use(VueSocketio, `${location.protocol}//${document.domain}:${location.port}`, store);

Vue.config.productionTip = false;
Vue.filter('score', score);
Vue.filter('teamName', teamName);

new Vue({
    el: "#app",
    store,
    render: h => h(App),
    components: {App},
    sockets: {
        connect: function() {
            this.$socket.emit('whoami');
        }
    }
});