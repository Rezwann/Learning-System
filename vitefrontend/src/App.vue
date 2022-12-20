<template>
    <nav class="container-fluid navbar navbar-expand-lg navbar-light bg-indigo-800">
      <h4 class="mx-4 text-white container-fluid">Rezwan: LMS</h4>
      <div class="navbar-nav ml-auto mx-4 mb-1 mt-1">
        <button
          class="nav-item nav-link btn btn-light mx-2 "
          @click="$router.push('/')"
        >
          Home
        </button>
        <button
          class="nav-item nav-link btn btn-light mx-2"
          @click="$router.push('/about')"
        >
          About
        </button>
        <template v-if="$store.state.isAuthenticated">
          <button
            class="nav-item nav-link btn btn-info mx-2"
            @click="$router.push('/overview')"
          >
            Overview
          </button>
          <button
            class="nav-item nav-link text-white btn btn-danger mx-2"
            @click="$router.push('/logout')">Logout
          </button>
        </template>
        <template v-else>
        <button
            class="nav-item nav-link btn btn-warning mx-2"
            @click="$router.push('/register')"
          >
            Register
          </button>
          <button
            class="nav-item nav-link text-white btn btn-secondary mx-2"
            @click="$router.push('/login')"
          >
            Login
          </button>

        </template>
      </div>
    </nav>
    <router-view></router-view>
  </template>
  
  
  
  <script>
  import axios from 'axios'

  export default {
    name: 'App',
    beforeCreate() {
      this.$store.commit('initalizeStore')
      const token = this.$store.state.token
  
      if (token) {
        axios.defaults.headers.common['Authorization'] = "Token" + token
      } else {
        axios.defaults.headers.common['Authorization'] = ""
      }
    }
  }
  </script>

<style>
.bg-indigo-800 {
  background-color: #5e00c3;
;
}
</style>