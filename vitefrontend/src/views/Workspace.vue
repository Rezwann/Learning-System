<template>
    <div class="mb-4"></div>
    <div>
      <h1 class="text-center mb-4">Learning Workspace</h1>
    </div>
  
    <div class="row align-items-start">
      <div v-for="board in LearningBoards">
        <div class="card mx-2 col-2">
          <div class="card-body">
            <h5 class="card-title">{{board.name}}</h5>
            <p class="card-text">{{board.short_description}}</p>
            <div v-for="card in LearningBoardsCards">
              <div v-if="card.learning_board_id == board.id">
                <div class="card">
                  {{card.id}}
                  <p>{{card.name}}</p>
                  <p>{{card.short_description}}</p>
                  <div v-for="list in LearningBoardsCardsLists">
                    <template v-if="list.learning_board_card_id == card.id">
                      {{ list.learning_board_card_id }}
                      {{ list.name }}
                    </template>
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
        LearningBoards: [],
        LearningBoardsCards: [],
        LearningBoardsCardsLists: []
      }
    },
    async mounted() {
      await axios.get('api/v1/LSM/getLearningBoards/').then(response => {
        this.LearningBoards = response.data
        console.log(this.LearningBoards)
      }),
      await axios.get('api/v1/LSM/getLearningBoardsCards/').then(response => {
        this.LearningBoardsCards = response.data
        console.log(this.LearningBoardsCards)
      }),
      await axios.get('api/v1/LSM/getLearningBoardsCardsLists/').then(response => {
        this.LearningBoardsCardsLists = response.data
        console.log(this.LearningBoardsCardsLists)
      })
      },
}
</script>

<style>
.scroll-row{
overflow-x: scroll;
}

</style>

<!--         <p>
  <button class="btn btn-primary btn-sm" type="button" data-bs-toggle="collapse" data-bs-target="#collapseExample" aria-expanded="false" aria-controls="collapseExample">
    See labels</button>
</p>
<div class="collapse" id="collapseExample">
  <div class="row align-items">
    <h6>
        Labels:
        <span class="fw-semibold badge text-bg-success mx-1 mt-1">🏷️ Cool</span>
        <span class="fw-semibold badge text-bg-success mx-1 mt-1">🏷️ Great</span>
        </h6>
</div>
</div>      -->