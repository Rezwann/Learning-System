<template>
    <div class="container-sm">
      <div class="mb-4"></div>
    <div><h1 class="text-center mb-4">Manage Teaching</h1></div>
    <div class="alert alert-danger" role="alert">

  <h4 class="alert-heading">Search for student</h4>
  <div class="row">
  <div class="col-8 mb-3">
    <select v-model="selectedStudent" class="form-control mt-3">
      <option value="">-- Select a student --</option>
      <option v-for="student in filtered" :value="student.username">{{ student.username }} ({{student.role}})</option>
    </select>
  </div>
  <div class="col-4 mt-3 mb-3">
    <button type="button" class="btn btn-primary" @click="GenerateInsight()">Select</button>
  </div>
</div>

  <hr>
      <h4 class="alert-heading">Manage Subject Content</h4>
  <p>

  </p>
  <hr>
  <h4 class="alert-heading">Add to Student's Individual Learning Workspace</h4>
  <p>.</p>
  <hr>


</div>
</div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Manage',
  data() {
    return {
      currentUser:'',    
      students: [],
      filtered:[],
      selectedStudent: '',  
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
    axios.get('/api/v1/LP/getCustomUsers/').then(response => {
      this.students = response.data
      this.filtered = this.students.filter(student => student.role === 'Student');
      
    })    
  },
  methods: {     

}
}
</script>