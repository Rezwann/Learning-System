<template>
    <div class="container">
      <div class="mb-4"></div>
      <h1 class="text-center">Log In</h1>
      <form @submit.prevent="submitForm" class="row mx-auto d-flex justify-content-center flex-column">
        <div class="col form-group mt-2">
          <label class="mb-2">Email </label>
          <input type="email" name="username" class="form-control" v-model="username">
        </div>
        <div class="col form-group mt-2">
          <label class="mb-2">Password 🔑</label>
          <input type="password" name="password" class="form-control" v-model="password">
        </div>
        <div v-if="errors.length" class="col">
          <p class="alert alert-info mt-3" role="alert" v-for="error in errors" v-bind:key="error">
            {{ error }}
          </p>
        </div>
        <div class="col d-flex justify-content-center mt-3">
          <button class="btn btn-success my-2">Log In</button>
        </div>
      </form>
      <div class="col d-flex justify-content-center mt-2">
      <button
            class="btn btn-primary my-2"
            @click="$router.push('/register')"
          >
            I need to create an account
          </button>
          </div>
    </div>
  </template>

<script>
import axios from 'axios';
export default {
    name:'Login',
    data(){
        return {
            username:'',
            password:'',
            errors:[]
        }
    },
    methods: {
        submitForm(e){
            axios.defaults.headers.common['Authorization'] = ""
            localStorage.removeItem("token")
            const formData = {
                username: this.username,
                password: this.password
            }
            axios.post("/api/v1/token/login/", formData)
            .then(response => {
                const token = response.data.auth_token

                this.$store.commit('setToken', token)
                
                axios.defaults.headers.common["Authorization"] = "Token " + token

                localStorage.setItem("token", token)
                
                this.$router.push('/overview')
            })
            .catch(error =>{
                if(error.response){
                    for (const item in error.response.data){
                        this.errors.push(`${error.response.data[item]}`)
                    }
                }
            })
        }
    }
}


</script> 