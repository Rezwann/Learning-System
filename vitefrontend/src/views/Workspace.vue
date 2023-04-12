<template >
<div class="mb-4"></div>
  <div>
    <h1 class="text-center">{{currentUser}}'s Learning Workspace</h1>
  </div>

  <div class="mx-3">
    <div class="container-fluid p-2 bg-indigo-400 mt-3 mb-3">
      <div class="row mt-2">
        <div class="col-sm-12 col-md-6 offset-md-3">
            <div class="card shadow-sm alert alert-warning">
  <form @submit.prevent="submitNewBoard();">
    <div class="row">
  <h5 class="card-text">Add a board</h5>
  
  <div class="col-4 mb-3">
    <label class="mb-1">Name</label>
    <input type="text" name="name" class="form-control" v-model="addBoardForm.name" placeholder="Name">
  </div>
  <div class="col-4 mb-3">
    <label class="mb-1">Short Description</label>
    <input
      type="text"
      name="short_description"
      class="form-control"
      v-model="addBoardForm.short_description" placeholder="Short Description"
    />
  </div>
  <div class="col-4 mt-4 mb-3">
    <button class="btn btn-warning">Add Board</button>
  </div>
  <span class="text-center error" v-if="errorMessage">{{ errorMessage }}</span>
</div>
  </form>
  <h6><em>Note: Green Learning boards = added by teacher, Yellow Learning boards = student</em></h6>

</div>
        </div>
      </div>
    </div>
</div>

  <div class="mx-3">
    <div class="container-fluid p-2 bg-indigo-400 mt-3 mb-4">
<div class="shadow-sm scroll-row" style="display: flex;">
        <div v-for="board in LearningBoards" :key ="board.id" style="flex-grow: 1;" class="mx-1">
          <div :class="{'shadow-sm alert alert-warning scrollable rounded mt-2': board.board_type === 'Student', 'shadow-sm alert alert-success scrollable rounded mt-2': board.board_type !== 'Student'}" style="width: 25vw;">
            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
            <button class="btn btn-sm btn-warning mb-2" @click="deleteBoard(board.id)">Delete Board</button>            
        </div>
            <h5 class="card-title">⭐ {{board.name}}</h5>
            <p class="card-text">{{board.short_description}}</p>
            <p class="card-subtitle text-muted">{{timeElapsed(board.created_at)}}</p>
            <hr>
            <div v-for="card in LearningBoardsCards">                
              <div v-if="card.learning_board_id == board.id">
                <div class="card mt-3 p-3 shadow-sm alert alert-info">
                  
                    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
            <button class="btn btn-sm btn-danger mx-1" @click="deleteCard(card.id)">Delete Card</button>            
        </div>        
                    <h6 class="card-title">{{card.name}}</h6>
                  <p class="card-text">{{card.short_description}}</p>
                    <div class="card-body">
                      <div v-for="list in LearningBoardsCardsLists">
                        <template v-if="list.learning_board_card_id == card.id">                            
  <div class="card shadow-sm alert alert-primary">
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

            
  <form v-if="currentBoardForm === board.id" @submit.prevent="addCard(board.id);">
  <div class="">
    <label class="">Name</label>
    <input type="text" name="name" class="form-control" v-model="newCard.name" placeholder="Name">
  </div>
  <div class="">
    <label class="">Short Description</label>
    <input type="text" name="description" class="form-control" v-model="newCard.description" placeholder="Description">
  </div>
  <div class="mt-3">
    <button class="btn btn-success" @click="currentBoardForm = board.id">Add Card</button>
  </div>
</form>

<button class="btn btn-sm btn-primary my-2" @click="currentBoardForm = currentBoardForm === board.id ? null : board.id">
  {{ currentBoardForm === board.id ? 'Hide' : 'Show' }} Add Card Form
</button>

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
        errorMessage:'',
        currentBoardForm: null,
        newCard: {
        board_id: null,
        name: '',
        description: ''
      },
        addBoardForm: {
            name:'',
            short_description:''
        },
        LearningWorkspace: [],
        LearningBoards: [],
        LearningBoardsCards: [],
        LearningBoardsCardsLists: [],
        LearningBoardsCardsListsItems: [],
        errors:[],
        id: 0,
        currentUser:'',
        currentUserRole: '',
      }
    },
    methods: {        
        timeElapsed(created_at) {
            const currentDate = moment()
            const createdAt = moment(created_at)
            const date = createdAt.format('MMM D, YYYY [at] h:mm A')
            const elapsed = moment.duration(currentDate.diff(createdAt)).humanize()
                    return `${date} (${elapsed} ago)`
        },
        async submitNewBoard(){
            if (this.addBoardForm.name && this.addBoardForm.short_description){
            await axios.post('api/v1/LP/addLearningBoard/', this.addBoardForm)
            .then(response => {
            }).catch(error =>{
                if(error.response){
                    for (const property in error.response.data){
                        this.errors.push(`${property}: ${error.response.data[property]}`)
                    }
                }
            })
            this.errorMessage = '';
            this.addBoardForm = {};
            } else {
                this.errorMessage = 'Both fields are required';
              }

            await axios.get('api/v1/LP/getLearningBoards/').then(response => {
            this.LearningBoards = response.data
            })
        },
        
        async deleteBoard(id) { 
          await axios.post('api/v1/LP/deleteLearningBoard/', {num:id})
          .then(response => {
          })

          await axios.get('api/v1/LP/getLearningBoards/').then(response => {
            this.LearningBoards = response.data
          })
        },
        async deleteCard(id) { 
          await axios.post('api/v1/LP/deleteLearningBoardCard/', {num:id})
          .then(response => {
          })

          await axios.get('api/v1/LP/getLearningBoardsCards/').then(response => {
            this.LearningBoardsCards = response.data
          })
        },
        async addCard(id) { 
          await axios.post('api/v1/LP/addLearningBoardCard/', {num:id, name:this.newCard.name, description:this.newCard.description})
          .then(response => {
          })

          this.newCard = { name: '', description: '' };
          this.currentBoardForm = null;          
          await axios.get('api/v1/LP/getLearningBoardsCards/').then(response => {
            this.LearningBoardsCards = response.data
          })
        },
    },
    async mounted() {
      await axios.get('api/v1/LP/getLearningWorkspace/').then(response => {
        this.LearningWorkspace = response.data
      }),
      await axios.get('api/v1/LP/getLearningBoards/').then(response => {
        this.LearningBoards = response.data
      }),
      await axios.get('api/v1/LP/getLearningBoardsCards/').then(response => {
        this.LearningBoardsCards = response.data
      }),
      await axios.get('api/v1/LP/getLearningBoardsCardsLists/').then(response => {
        this.LearningBoardsCardsLists = response.data
      }),
      await axios.get('api/v1/LP/getLearningBoardsCardsListsItems/').then(response => {
        this.LearningBoardsCardsListsItems = response.data
      }),
      await axios.get('/api/v1/LP/getCurrentUser/').then(response => {
        this.currentUser = response.data.username
        this.currentUserRole = response.data
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