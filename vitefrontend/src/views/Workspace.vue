<template>
    <div class="mb-4"></div>
    <div>
      <h1 class="text-center mb-4">Learning Workspace</h1>
    </div>

    <div class="d-flex flex-wrap">
      <div v-for="board in LearningBoards" class="mx-2">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{board.name}}</h5>
            <p class="card-text">{{board.short_description}}</p>
            <div v-for="card in LearningBoardsCards">
              <div v-if="card.learning_board_id == board.id">
                <div class="card mt-3 p-3">
                  <h6 class="card-title">{{card.name}}</h6>
                  <p class="card-text">{{card.short_description}}</p>
                  <div class="card mt-3">
                    <div class="card-body">
                      <div v-for="list in LearningBoardsCardsLists">
                        <template v-if="list.learning_board_card_id == card.id">
                          <div class="card mt-3">
                            <div class="card-body">
                              <p>{{ list.name }}</p>
                              {{list.short_description}}
                            </div>
                          </div>
                        </template>
                      </div>
                    </div>
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