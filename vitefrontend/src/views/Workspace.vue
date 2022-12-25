<template >
<div class="mb-4"></div>
  <div>
    <h1 class="text-center">Learning Workspace</h1>
  </div>
  <div class="mx-3">
    <div class="container-fluid p-2 bg-indigo-400 mt-3">
<div class="shadow-sm scroll-row" style="display: flex;">
        <div v-for="board in LearningBoards" style="flex-grow: 1;" class="mx-1">
        <div style="width: 25vw;" class="shadow-sm alert alert-warning scrollable rounded mt-2">
          <div class="">
            <h5 class="card-title">{{board.name}}</h5>
            <p class="card-text">{{board.short_description}}</p>
            <p class="card-subtitle text-muted">{{timeElapsed(board.created_at)}}</p>
            <hr>
            <div v-for="card in LearningBoardsCards">
              <div v-if="card.learning_board_id == board.id">
                <div class="card mt-3 p-3 shadow-sm alert alert-info">
                  <h6 class="card-title">{{card.name}}</h6>
                  <p class="card-text">{{card.short_description}}</p>
                  
                  
<!-- only show see tags if card has tags -->
 <div id="tag-related" class="d-flex align-items-center">
                   <template v-if="LearningBoardsCardsTags.some(tag => tag.related_card_id == card.id)">
  <p><button class="btn btn-primary btn-sm" type="button" data-bs-toggle="collapse" v-bind:data-bs-target="'#tags' + card.id" aria-expanded="false" v-bind:aria-controls="'tags' + card.id">Tags</button></p>
</template>

<div class="collapse" v-bind:id="'tags' + card.id">
      <div class="row align-items">
        <h6 class="mx-2 mb-3">
          
          <template v-for="tag in LearningBoardsCardsTags">
            <template v-if="tag.related_card_id == card.id">
              <span class="fw-semibold badge text-bg-success mx-1 mt-1">🏷️ {{tag.name}}</span>
            </template>
          </template>
        </h6>
      </div>
    </div>
</div>
                    <div class="card-body">
                      <div v-for="list in LearningBoardsCardsLists">
                        <template v-if="list.learning_board_card_id == card.id">                            
  <div class="card shadow-sm alert alert-success">
    <div class="card-body">
      <h6>{{ list.name }}</h6>
      <p>{{list.short_description}}</p>
    </div>

    <div v-for="item in LearningBoardsCardsListsItems">
      <div v-if="item.learning_board_card_list_id == list.id">
        <li>{{item.name}}</li>
      </div>                        
    </div>

    <template v-if="!LearningBoardsCardsListsItems.some(item => item.learning_board_card_list_id == list.id)">
      <p>An item is yet to be added to this list</p>
    </template>
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
  </div>    
</template>


<script>
  import axios from 'axios'
  import moment from 'moment'
  export default {
    name: 'Workspace',
    data() {
      return {
        LearningBoards: [],
        LearningBoardsCards: [],
        LearningBoardsCardsLists: [],
        LearningBoardsCardsListsItems: [],
        LearningBoardsCardsTags:[]
      }
    },
    methods: {        
    timeElapsed(created_at) {
      const currentDate = moment()
      const createdAt = moment(created_at)
      const date = createdAt.format('MMM D, YYYY [at] h:mm A')
      const elapsed = moment.duration(currentDate.diff(createdAt)).humanize()
    return `${date} (${elapsed} ago)`
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
      await axios.get('api/v1/LSM/getLearningBoardsCardsTags/').then(response => {
        this.LearningBoardsCardsTags = response.data
        console.log(this.LearningBoardsCardsTags)
      })
      await axios.get('api/v1/LSM/getLearningBoardsCardsLists/').then(response => {
        this.LearningBoardsCardsLists = response.data
        console.log(this.LearningBoardsCardsLists)
      }),
      await axios.get('api/v1/LSM/getLearningBoardsCardsListsItems/').then(response => {
        this.LearningBoardsCardsListsItems = response.data
        console.log(this.LearningBoardsCardsListsItems)
      })
      },
}
</script>

<style>
.scroll-row{
overflow-x: scroll;
max-width: 100%; 
}

.scroll-row::-webkit-scrollbar {
    border-radius: 10rem;
    background-color: #f1f1f19a;
    width: 0.55rem;
}

.scroll-row::-webkit-scrollbar-thumb {
  border-radius: 1rem;
  margin: 1rem;
  background-color: #ffa0a0;
}

.scroll-row::-webkit-scrollbar-thumb:hover {
  border-radius: 1rem;
  margin: 1rem;
  background-color: #ff4b4b;
}

.scrollable {
  overflow-y: scroll;
  max-height: 65vh; 

}

.scrollable::-webkit-scrollbar {
    border-radius: 10rem;
    background-color: #f1f1f19a;
    width: 0.75rem;
}

.scrollable::-webkit-scrollbar-thumb {
  border-radius: 1rem;
  margin: 1rem;
  width: 0.75rem;
  background-color: #ffd856;
}

.scrollable::-webkit-scrollbar-thumb:hover {
  border-radius: 1rem;
  margin: 1rem;
  width: 0.75rem;
  background-color: #facb30;
}

.bg-indigo-400 {
  background-color: #c3000020;
}

</style>