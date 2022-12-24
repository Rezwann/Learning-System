<template> 
<div class="mb-4"></div>
    <div><h1 class="text-center mb-4">Workspace</h1></div>

    <div class="scroll-row alert alert-warning">
    <div class="">
  <div class='row align-items-start flex-nowrap'>

    <div v-for="board in LearningBoards">
    <div class="card mx-2 col-2">
      <div class="card-body">

    
        <h5 class="card-title">{{board.name}}</h5>
        <p class="card-text">{{board.short_description}}</p>

        <p>
  <button class="btn btn-primary btn-sm" type="button" data-bs-toggle="collapse" data-bs-target="#collapseExample" aria-expanded="false" aria-controls="collapseExample">
    See labels</button>
</p>
<div class="collapse" id="collapseExample">
  <div class="row align-items">
    <h6>
        Labels:
        <span class="fw-semibold badge text-bg-success mx-1 mt-1">🏷️ Cool</span>
        <span class="fw-semibold badge text-bg-success mx-1 mt-1">🏷️ Great</span>
        <span class="fw-semibold badge text-bg-success mx-1 mt-1">🏷️ Nice</span>
        <span class="fw-semibold badge text-bg-success mx-1 mt-1">🏷️ Awesome</span>
        </h6>
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
    name: 'Workspace',
    data() {
      return {
        LearningBoards: []
      }
    },
    async mounted() {
      await axios.get('api/v1/LSM/getLearningBoards/').then(response => {
        this.subjectAreas = response.data
        this.LearningBoards = response.data
        console.log(this.LearningBoards)
      })
      },
}
</script>

<style>
.scroll-row{
overflow-x: scroll;
}

</style>