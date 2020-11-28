import variables from '../sass/_variables.scss';

window.variables = variables;
window.Vue = require('vue');

Vue.component('field-input', require('./components/input-field').default);

const app = new Vue({
    el: '#app',
    data: {}
});
