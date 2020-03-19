import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from '../components/HelloWorld.vue';


Vue.use(Router);

export default new Router ({
    mode :'history',
    base : 'http://localhost:8080',
    routes: [
        {
            path: '/ping',
            name: 'HelloWorld',
            component: HelloWorld,
        }
    ],
})