import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import store from './store'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(),
    routes: []
})

createApp(App).use(store).use(router).mount('#app')