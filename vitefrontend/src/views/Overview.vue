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
  
    <div class="accordion alert alert-info container-md">
        <div v-if="filteredSubjects.length === 0">
            <h2 class="text-center mt-4 mb-4">No subjects</h2>
        </div>
        <div v-for="subject in filteredSubjects" v-bind:key="subject.id">
        <div class="accordion-item mt-2 mb-2">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" v-bind:data-bs-target="'#accordion-item-' + subject.id" aria-expanded="false" v-bind:aria-controls="'accordion-item-' + subject.id">
              {{subject.name}} - Subject Code: {{subject.subject_code}}
            </button>
          </h2>
          <div v-bind:id="'accordion-item-' + subject.id" class="accordion-collapse collapse" v-bind:aria-labelledby="'accordion-item-' + subject.id">
            <div class="accordion-body">
              <p><strong>Name: </strong>{{subject.name}}</p>
              <p><strong>Details: </strong>{{subject.details}}</p>
              <p><strong>Subject Category: </strong>{{subject.category_name}}</p>
              <p><strong>Year Group: </strong>{{subject.year_group}}</p>
              <p><strong>Subject Leader Name: </strong>{{subject.subject_leader_name}}</p>
              <p><strong>Subject Leader Contact Email: </strong>{{subject.subject_leader_email}}</p>
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
      await axios.get('api/v1/subjects/subjectCategories/').then(response => {
        this.subjectAreas = response.data
        console.log(response)
      })
  
      await axios.get('/api/v1/subjects').then(response => {
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
</style>

<!-- <button class="btn btn-primary mx-3 mb-4" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasExample" aria-controls="offcanvasExample">
    Button with data-bs-target
  </button>
  
  <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasExample" aria-labelledby="offcanvasExampleLabel">
    <div class="offcanvas-header">
      <h5 class="offcanvas-title" id="offcanvasExampleLabel">Offcanvas</h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      <div>
        Some text as placeholder. In real life you can have the elements you have chosen. Like, text, images, lists, etc.
      </div>
    </div>
  </div> -->