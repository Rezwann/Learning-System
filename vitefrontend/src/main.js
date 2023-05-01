import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import StudentProfile from './views/StudentProfile.vue'
import Overview from './views/Overview.vue'
import Workspace from './views/Workspace.vue'
import Logout from './views/Logout.vue'
import Register from './views/Register.vue'
import Login from './views/Login.vue'
import Manage from './views/Manage.vue'
import store from './store'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.css'
import VCalendar from 'v-calendar';
import 'v-calendar/dist/style.css';

axios.defaults.baseURL = 'http://127.0.0.1:8000'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'Home', component: Home },
        { path: '/register', name: 'Register', component: Register },
        { path: '/login', name: 'Login', component: Login },
        {
            path: '/studentprofile',
            name: 'StudentProfile',
            component: StudentProfile,
            meta: {
                requireAuthentication: true
            }
        },
        {
            path: '/overview',
            name: 'Overview',
            component: Overview,
            meta: {
                requireAuthentication: true
            }
        },
        {
            path: '/workspace',
            name: 'Workspace',
            component: Workspace,
            meta: {
                requireAuthentication: true
            }
        },
        {
            path: '/logout',
            name: 'Logout',
            component: Logout,
            meta: {
                requireAuthentication: true
            }
        },
        {
            path: '/manage',
            name: 'Manage',
            component: Manage,
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

createApp(App).use(store).use(router, axios).use(VCalendar, {}).mount('#app')
import 'bootstrap/dist/js/bootstrap.js'