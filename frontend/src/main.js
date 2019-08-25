import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import Resource from 'vue-resource';

Vue.use(Resource);
Vue.config.productionTip = false;

new Vue({
  vuetify,
  render: h => h(App),
}).$mount("#app");