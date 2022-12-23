<template>
    <div class="container">
      <div class="mb-4"></div>
      <h1 class="text-center">Register</h1>
      <form @submit.prevent="submitForm" class="row mx-auto d-flex justify-content-center flex-column">
        <div class="col form-group mt-2">
          <label class="mb-2">Username</label>
          <input type="text" name="username" class="form-control" v-model="username">
        </div>
        <div class="col form-group mt-2">
          <label class="mb-2">Email</label>
          <input type="email" name="email" class="form-control" v-model="email">
        </div>
        <div class="col form-group mt-2">
          <label class="mb-2">Password 🔑</label>
          <input type="password" name="password" class="form-control" v-model="password">
        </div>
        <div class="col form-group mt-2">
          <label class="mb-2">Enter Password Again 🔑</label>
          <input type="password" name="password" class="form-control" v-model="password2">
        </div>
        <div v-if="errors.length" class="col">
          <p class="alert alert-info mt-3" role="alert" v-for="error in errors" v-bind:key="error">
            {{ error }}
          </p>
        </div>
        <div class="col d-flex justify-content-center mt-3">
          <button class="btn btn-success my-2">Register </button>
        </div>
      </form>
      <div class="col d-flex justify-content-center mt-2">
        <button
            class="btn btn-primary my-2"
            @click="$router.push('/login')"
          >
            I already have an account
          </button>
        </div>

        </div>
  </template>  
  

<script>
import axios from 'axios';
export default {
    name:'Register',
    data(){
        return {
            username:'',
            email:'',
            password:'',
            password2:'',
            errors:[]    
    }
    },
    methods:{
        submitForm(e){

          this.errors = []

          if (this.password !== this.password2){
            this.errors.push('Entered passwords do not match')
          }

          if (this.errors.length == 0){
            
            const formData = {
                username: this.username,
                password: this.password,
                email: this.email
            }

            axios.post("/api/v1/users/", formData)
            .then(response => {
                console.log(response)                
                this.$router.push('/login')
            })
            .catch(error =>{
                if(error.response){
                    for (const property in error.response.data){
                        this.errors.push(`${property}: ${error.response.data[property]}`)
                    }
                }
            })
          }
        }
    }
}

</script>