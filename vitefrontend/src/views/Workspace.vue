<template> 

<div class="mb-4"></div>
    <div><h1 class="text-center mb-4">Workspace</h1></div>

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