import { createStore } from 'vuex'

export default createStore({
    state: {
        user: {
            username: ''
        },
        isAuthenticated: false,
        token: '',
        refresh: ''
    },
    mutations: {
        initalizeStore(state) {
            if (localStorage.getItem('token')) {
                state.token = localStorage.getItem('token')
                state.isAuthenticated = true
            } else {
                state.token = ''
                state.isAuthenticated = false
            }
        },
        setToken(state, token) {
            state.token = token
            state.isAuthenticated = true
        },
        removeToken(state) {
            state.token = ''
            if (state.isAuthenticated = true) {
                state.isAuthenticated = false
            }
        },
        setRefresh(state, refresh) {
            state.refresh = refresh
        }
    },
    actions: {

    },
    modules: {

    }
})