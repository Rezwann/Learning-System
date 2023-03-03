<template>
    <div class="container-sm">
      <div class="mb-4"></div>
    <div><h1 class="text-center mb-4">Manage Teaching</h1></div>
    <div class="alert alert-danger" role="alert">
  <h4 class="alert-heading">Manage Subject Content</h4>
  <p>.</p>
  <hr>
  <h4 class="alert-heading">Add to Student's Individual Learning Workspace</h4>
  <p>.</p>
  <hr>
  <h4 class="alert-heading">Manage Student's Insight Assessments</h4>
  <p>.</p>

</div>
</div>
</template>

<script>
import axios from 'axios'
import moment from 'moment'

export default {
  name: 'Manage',
  data() {
    return {
      currentUser:'',      
    }
  },
  async mounted() {
    await axios.get('/api/v1/LP/getCurrentUser/').then(response => {
      this.currentUser = response.data.username
    })
  },
  created(){
    axios.get('/api/v1/LP/getCurrentUser/').then(response => {
      this.currentUser = response.data.username
    })
    axios.get('/api/v1/LP/getMyTeachingSubjects/').then(response => {
      console.log(response.data)
    })
  },
  methods: {     

}
}
</script>