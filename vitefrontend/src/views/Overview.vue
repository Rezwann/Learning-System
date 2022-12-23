<template>
    <div class="mb-4"></div>
<div><h1 class="text-center">Overview</h1></div>

<button class="btn btn-primary mx-3 mb-4" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasExample" aria-controls="offcanvasExample">
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
</div>

<div class="">
    <ul class=" mx-2 list-group list-group-horizontal">
  <li class="list-group-item active">An item</li>
  <li class="list-group-item">A second item</li>
  <li class="list-group-item">A third item</li>
  <li class="list-group-item">A third item</li>
  <li class="list-group-item">A third item</li>
  <li class="list-group-item">A third item</li>
</ul>
</div>



<!-- <div class="container-sm mb-4">
<div class="progress">
  <div class="progress-bar progress-bar-striped bg-primary" role="progressbar" aria-label="Warning striped example" style="width: 75%" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">75%</div>
</div>
</div> -->



<div class="accordion" id="">
    <div v-for="subject in subjects" v-bind:key="subject.id">
    <div class="accordion-item">
        <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" v-bind:data-bs-target="'#accordion-item-' + subject.id" aria-expanded="false" v-bind:aria-controls="'accordion-item-' + subject.id">
                {{subject.name}}
            </button>
        </h2>
        <div v-bind:id="'accordion-item-' + subject.id" class="accordion-collapse collapse" v-bind:aria-labelledby="'accordion-item-' + subject.id">
            <div class="accordion-body">
                <p><strong>Name: </strong>{{subject.name}}</p>
                <p><strong>Details: </strong>{{subject.details}}</p>
                <p><strong>Category: </strong>{{subject.category}}</p>
                <p><strong>Year Group: </strong>{{subject.year_group}}</p>
                <p><strong>Subject Leader: </strong>{{subject.subject_leader}}</p>
            </div>
        </div>
    </div>
</div>

</div>

<nav aria-label="Page navigation example">
  <ul class="pagination justify-content-center mt-3">

    <li class="page-item active"><a class="page-link" href="#">1</a></li>
    <li class="page-item"><a class="page-link" href="#">2</a></li>
    <li class="page-item"><a class="page-link" href="#">3</a></li>
  </ul>
</nav>

</template>

<script>
import axios from 'axios'
export default {
    name: 'Overview',
    data(){
        return {
            subjects: []
        }
    },
    mounted(){

        axios.get('/api/v1/subjects').then(response =>{
            this.subjects = response.data
        })
    }
}
</script>