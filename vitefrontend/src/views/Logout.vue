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
    methods: {
  async logout() {
    try {
      await axios.post("/api/v1/token/logout/");
      axios.defaults.headers.common['Authorization'] = "";
      localStorage.removeItem('token');
      localStorage.clear();
      sessionStorage.clear();
      this.$store.commit("removeToken");
      this.$router.push("/");
    } catch (error) {
      console.error(error);
    }
  }
}

}
</script>