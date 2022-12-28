<template>
    <div class="mb-4"></div>
    <div><h1 class="text-center mb-4">{{currentUser}}'s Overview</h1></div>
  
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
  
    <div class="accordion alert alert-info mx-4" id ="main-accordion">
        <div v-if="filteredSubjects.length === 0">
            <h2 class="text-center mt-4 mb-4">No subjects</h2>
        </div>
        <div v-for="subject in filteredSubjects" v-bind:key="subject.id">
        <div class="accordion-item mt-2 mb-2">
          <h2 class="accordion-header">
            <button @click="resetCommunicationArea" class="accordion-button collapsed" type="button"  data-bs-toggle="collapse" v-bind:data-bs-target="'#accordion-item-' + subject.id" aria-expanded="false" v-bind:aria-controls="'accordion-item-' + subject.id">
              ⭐ {{subject.name}} ({{subject.subject_code}}) - {{subject.category_name}}
            </button>
          </h2>
          <div v-bind:id="'accordion-item-' + subject.id" class="accordion-collapse collapse" data-bs-parent="#main-accordion" v-bind:aria-labelledby="'accordion-item-' + subject.id">

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

<!-- communication area channels -->
        <div class="row">
  <div class="col-4 rounded" style="height: 40vh; background-color: var(--dark-purple);">
    <nav class="flex-column mt-4">
      <nav class="nav flex-column mx-2">
        <div v-for="Area in communicationArea.communicationAreas">
  <div v-if="Area.related_subject_id == subject.id">
    
    <h6 class="text-white font-weight-bold">{{Area.name}}</h6>
    <a class="nav-link text-white font-weight-bold rounded mt-2" style="background-color: var(--dark-gray);">Channels</a>  
    <div v-for="channel in communicationArea.communicationChannels">
    <div v-if="channel.communication_area_id == Area.id">
      <nav class="nav flex-column mt-2 hover">
              <a @click="displayChannel(channel)" class="btn nav-link ms-4 my-1 text-white rounded" style="background-color: var(--light-gray);">{{ channel.name }}</a>
        </nav>        
    </div>    
    </div>
  </div>
</div>
      </nav>
    </nav>
  </div>

  <!-- communication area main content -->
  <div class="col-8 text-white">
    <div class="p-3 rounded" style="background-color: var(--dark-purple);">
      <h4>{{communicationArea.currentChannelName}}</h4>
      <div class="scrollable-g" style="height: 40vh;">
        <div v-if="communicationArea.displayChannelClicked && communicationArea.currentChannelPosts.length === 0">
          no content </div><div v-else><div v-if="communicationArea.currentChannelPosts.length === 0">browse</div>
</div>
      <div v-for="post in communicationArea.currentChannelPosts">
      <div class="mb-2 alert alert-secondary mx-2">
        <div class="d-flex">
          <img src="https://via.placeholder.com/50x50" alt="Avatar" class="rounded mx-2">
          <div>
            <h6 class="mb-0">{{post.author_username}} ({{ post.author_role }})</h6>
            <small>{{timeElapsed(post.created_at)}}</small>
          </div>
        </div>
        <p class="mb-0 mt-3">{{post.content}}</p>
      </div>
            </div></div>                
</div>


    <div class="p-3 mt-2 rounded" style="background-color: var(--dark-purple);">
          <!-- Input field for posting messages -->
          <form @submit.prevent="addChannelPost()">
        <div class="form-group">
          <input v-model="communicationArea.channelPost" type="text" class="form-control" placeholder="Type a message...">
          <button type="submit" class="btn btn-success mt-2">Send</button>
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
  import moment from 'moment'
  export default {
    name: 'Overview',
    data() {
      return {
        currentUser:'',
        subjectAreas: [],
        subjects: [],
        filteredSubjects: [],
        currentSubjectArea: '',
        communicationArea: {
          communicationAreas:[],
          communicationChannels:[],
          currentChannelName:'',
          currentChannelPosts:[],
          displayChannelClicked: false,
          currentChannelID: null,
          currentChannel: [],
          channelPost:''
        }
      }
    },
    async mounted() {
      await axios.get('api/v1/LP/subjectCategories/').then(response => {
        this.subjectAreas = response.data
        console.log(response)
      })
  
      await axios.get('/api/v1/LP').then(response => {
        this.subjects = response.data
        console.log(response.data)
        this.filteredSubjects = this.subjects
      })

      await axios.get('/api/v1/LP/getCommunicationAreas/').then(response => {
        this.communicationArea.communicationAreas = response.data
      })

      await axios.get('/api/v1/LP/getCommunicationChannels/').then(response => {
        this.communicationArea.communicationChannels = response.data
        
      })
      
      await axios.get('/api/v1/LP/getCurrentUser/').then(response => {
        this.currentUser = response.data.username
      })
    },
    methods: {
      timeElapsed(created_at) {
            const currentDate = moment()
            const createdAt = moment(created_at)
            const date = createdAt.format('MMM D, YYYY [at] h:mm A')
            const elapsed = moment.duration(currentDate.diff(createdAt)).humanize()
                    return `${date} (${elapsed} ago)`
        },
      async displayChannel(channel) {
        this.communicationArea.currentChannel = channel;
        this.communicationArea.currentChannelID = channel.id;
        this.communicationArea.displayChannelClicked = true;
        this.communicationArea.currentChannelName = channel.name;
        console.log(channel.id)
        await axios.post('api/v1/LP/getCommunicationChannelPosts/', {num:channel.id})
          .then(response => {
            this.communicationArea.currentChannelPosts = response.data
      })        
  },
    async addChannelPost(){
      if (this.communicationArea.currentChannelID){
        await axios.post('api/v1/LP/addCommunicationChannelPost/', {num:this.communicationArea.currentChannelID, content:this.communicationArea.channelPost})
          .then(response => {
      })     
      this.displayChannel(this.communicationArea.currentChannel) 
      this.communicationArea.channelPost = '' 
      }      
    },
    async resetCommunicationArea() {
      this.communicationArea.currentChannel = [];
      this.communicationArea.currentChannelPosts = [];
        this.communicationArea.currentChannelID = null;
        this.communicationArea.displayChannelClicked = false;
        this.communicationArea.currentChannelName = 'Browse a channel',
      await axios.get('/api/v1/LP/getCommunicationAreas/').then(response => {
        this.communicationArea.communicationAreas = response.data
      })

      await axios.get('/api/v1/LP/getCommunicationChannels/').then(response => {
        this.communicationArea.communicationChannels = response.data
        
      })
    },

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
  background-color: #6800d7;
}

:root {
    --light-gray: #4b009b;
    --dark-gray: #6800d7;
    --dark-purple: #2d005d;
  }


  .scrollable-g {
  overflow-y: scroll;
  max-height: 60vh; 

}

.scrollable-g::-webkit-scrollbar {
    border-radius: 10rem;
    background-color: #f1f1f19a;
    width: 0.75rem;
}

.scrollable-g::-webkit-scrollbar-thumb {
  border-radius: 1rem;
  margin: 1rem;
  width: 0.75rem;
  background-color: rgb(0, 158, 13);
}

.scrollable-g::-webkit-scrollbar-thumb:hover {
  border-radius: 1rem;
  margin: 1rem;
  width: 0.75rem;
  background-color: rgb(0, 192, 16);
}
</style>