import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import About from './views/About.vue'
import Overview from './views/Overview.vue'
import Register from './views/Register.vue'
import Login from './views/Login.vue'
import store from './store'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.css'

axios.defaults.baseURL = 'http://127.0.0.1:8000'

const router = createRouter({
    history: createWebHistory(),
    routes: [{
            path: '/',
            name: 'Home',
            component: Home
        },
        {
            path: '/about',
            name: 'About',
            component: About
        },
        {
            path: '/register',
            name: 'Register',
            component: Register
        },
        {
            path: '/login',
            name: 'Login',
            component: Login
        },
        {
            path: '/overview',
            name: 'Overview',
            component: Overview,
            meta: {
                requireAuthentication: true
            }
        }
    ]
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requireAuthentication) && !store.state.isAuthenticated) {
        next('/login')
    } else {
        next()
    }
})

createApp(App).use(store).use(router, axios).mount('#app')

import 'bootstrap/dist/js/bootstrap.js'