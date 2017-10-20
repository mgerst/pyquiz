import Vue from 'vue'
import App from './App.vue'
import score from './filters/score'
import store from './store'

Vue.config.productionTip = false;
Vue.filter('score', score);

new Vue({
    el: "#app",
    store,
    render: h => h(App),
    components: {App}
});