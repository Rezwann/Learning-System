<template>
    <div class="mb-4"></div>
    <div><h1 class="text-center">Overview</h1></div>
  
    <div>
      <ul class=" col d-flex justify-content-center mb-4 mt-2 mx-2 list-group list-group-horizontal">

        <li class="btn list-group-item mx-1" :class="{'active': currentSubjectArea === ''}" @click="filterSubjects('')">All
            <span class="badge bg-secondary rounded-pill">{{subjects.length}}</span>

        </li>
        <div v-for="area in subjectAreas">
            <li class="btn list-group-item mx-1" :class="{'active': area.name === currentSubjectArea}" @click="filterSubjects(area.name)">{{area.name}}
            </li> 
        </div>
        </ul>
    </div>
  
    <div class="accordion alert alert-info mx-4">
        <div v-if="filteredSubjects.length === 0">
            <h2 class="text-center mt-4 mb-4">No subjects</h2>
        </div>
        <div v-for="subject in filteredSubjects" v-bind:key="subject.id">
        <div class="accordion-item mt-2 mb-2">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" v-bind:data-bs-target="'#accordion-item-' + subject.id" aria-expanded="false" v-bind:aria-controls="'accordion-item-' + subject.id">
              ⭐ {{subject.name}} ({{subject.subject_code}}) | {{subject.category_name}}
            </button>
          </h2>
          <div v-bind:id="'accordion-item-' + subject.id" class="accordion-collapse collapse" v-bind:aria-labelledby="'accordion-item-' + subject.id">
            <div class="accordion-body">
              <div class="alert alert-success">
  <div class="row">
    <div class="col-6">
      <p><strong>Details: </strong>{{subject.details}}</p>
    </div>
    <div class="col-6">
      <p><strong>Year Group: </strong>{{subject.year_group}}</p>
    </div>
  </div>
  <div class="row">
    <div class="col-6">
      <p><strong>Subject Leader Name: </strong>{{subject.subject_leader_name}}</p>
    </div>
    <div class="col-6">
      <p><strong>Subject Leader Contact Email: </strong>{{subject.subject_leader_email}}</p>
    </div>
  </div>
</div>              
              <div class="row">
  <div class="col-4 bg-dark rounded">
    <nav class="flex-column">
      <nav class="nav flex-column">
        <a class="nav-link text-white font-weight-bold" style="background-color: var(--dark-gray);">Item 1</a>
        <nav class="nav flex-column">
          <a class="nav-link ms-3 my-1 text-white" style="background-color: var(--light-gray);">Item 1-1</a>
          <a class="nav-link ms-3 my-1 text-white" style="background-color: var(--light-gray);">Item 1-2</a>
        </nav>
        <a class="nav-link text-white font-weight-bold" style="background-color: var(--dark-gray);">Item 2</a>
        <nav class="nav flex-column">
          <a class="nav-link ms-3 my-1 text-white" style="background-color: var(--light-gray);">Item 2-1</a>
          <a class="nav-link ms-3 my-1 text-white" style="background-color: var(--light-gray);">Item 2-2</a>
        </nav>
      </nav>
    </nav>
  </div>
  <div class="col-8">
    <div class="p-3 alert-success alert rounded">
      <h4>Item 1</h4>
      <div class="mb-4 alert alert-secondary">
        <div class="d-flex">
          <img src="https://via.placeholder.com/50x50" alt="Avatar" class="rounded mx-2">
          <div>
            <h5 class="mb-0">Username</h5>
            <small>12:34 PM</small>
          </div>
        </div>
        <p class="mb-0 mt-3">This is an example message.</p>
      </div>
      <div class="mb-4 alert alert-secondary">
        <div class="d-flex">
          <img src="https://via.placeholder.com/50x50" alt="Avatar" class="rounded mx-2">
          <div>
            <h5 class="mb-0">Username</h5>
            <small>12:34 PM</small>
          </div>
        </div>
        <p class="mb-0 mt-3">This is an example message.</p>
      </div>
      <div class="mb-4 alert alert-secondary">
        <div class="d-flex align-items-center">
          <img src="https://via.placeholder.com/50x50" alt="Avatar" class="rounded mx-2">
          <div>
            <h5 class="mb-0">Username</h5>
            <small>12:35 PM</small>
          </div>
        </div>
        <p class="mb-0 mt-3">And another example message.</p>
      </div>
      
      <!-- Input field for posting messages -->
      <form @submit.prevent="">
        <div class="form-group">
          <input type="text" class="form-control" placeholder="Type a message...">
          <button type="submit" class="btn btn-primary mt-2">Send</button>
        </div>
      </form>
    </div>
  </div>
</div>  





</div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'Overview',
    data() {
      return {
        subjectAreas: [],
        subjects: [],
        filteredSubjects: [],
        currentSubjectArea: ''
      }
    },
    async mounted() {
      await axios.get('api/v1/LP/subjectCategories/').then(response => {
        this.subjectAreas = response.data
        console.log(response)
      })
  
      await axios.get('/api/v1/LP').then(response => {
        this.subjects = response.data
        this.filteredSubjects = this.subjects
      })
    },
    methods: {
  filterSubjects(category) {
    this.currentSubjectArea = category
    if (category === '') {
      this.filteredSubjects = this.subjects
    } else {
      this.filteredSubjects = this.subjects.filter(subject => subject.category_name === category)
    }
  }
}
}
</script>

<style>
.bg-indigo-800 {
  background-color: #5e00c3;
}

:root {
    --light-gray: #2f3136;
    --dark-gray: #23272a;
  }
</style>