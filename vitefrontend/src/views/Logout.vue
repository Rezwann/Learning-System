<template>
          <div class="mb-4"></div>
<h1 class="text-center">Are you sure you want to log out? 🤔</h1>

<div class="d-flex justify-content-center mt-4">
  <button @click="logout()" class="btn btn-danger text-center">Yes, Log Out</button>
</div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Logout',
    methods:{
        logout(){
            axios.post("/api/v1/token/logout/").then(response => {
            axios.defaults.headers.common['Authorization'] = ""
            localStorage.removeItem("token")
            this.$store.commit('removeToken')
            this.$router.push('/')
            })
        }
    }
}
</script>