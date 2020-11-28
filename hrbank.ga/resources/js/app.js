import Multiselect from "vue-multiselect";

window.Vue = require('vue');

Vue.component('field-input', require('./components/field-input').default);
Vue.component('field-select', require('./components/field-select').default);
Vue.component('tabs', require('./components/tabs').default);
Vue.component('list', require('./components/list').default);
Vue.component('requirements', require('./components/requirements').default);
Vue.component('multiselect', Multiselect);

const app = new Vue({
    el: '#app',
    data: {

    }
});
