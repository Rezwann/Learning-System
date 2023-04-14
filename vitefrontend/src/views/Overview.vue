<template>
    <div class="mb-4"></div>
    <div><h1 class="text-center mb-4">{{currentUser}}'s Overview</h1></div>

  <div v-if="currentUserRole == 'Teacher'">
    <div class="card mt-3 p-3 mx-auto alert alert-warning" style="width:80vw;">
  <h6 class="card-subtitle text-muted text-center"> As you have {{currentUserRole}} role, you may create subject areas. 
    These will be visible below with additional management options. You can search for a student in 'Manage Teaching' to add individual students to your created subject areas and for more specific learning management options.</h6>
  </div>  

  <div class="card mt-3 p-3 alert alert-warning mx-auto" style="width:80vw;">
<h4 class="text-center mb-4">Create a Subject Area</h4>
<form @submit.prevent="createSubjectForOverview();">
    <div class="row">  
      <div class="col-4 mb-3">
    <label class="mb-1">Subject Choice</label>
    <select
        v-model="createSubject.subjectchoice"
        class="form-select form-select mb-3"
        aria-label=".form-select"
      >
        <option selected disabled value="">Select from subject choice</option>
        <option v-for="choice in subjectChoices" :key="choice" :value="choice">
          {{choice}}
        </option>
      </select>
  </div>      

  <div class="col-4 mb-3">
    <label class="mb-1">Year Group</label>
    <select
        v-model="createSubject.yearchoice"
        class="form-select form-select mb-3"
        aria-label=".form-select"
      >
        <option selected disabled value="">Select from year groups</option>
        <option v-for="choice in yearChoices" :key="choice" :value="choice">
          {{choice}}
        </option>
      </select>
  </div>  

      <div class="col-4 mb-3">
    <label class="mb-1">Subject Category</label>
    <select
        v-model="createSubject.categorychoice"
        class="form-select form-select mb-3"
        aria-label=".form-select"
      >
        <option selected disabled value="">Select from subject categories</option>
        <option v-for="choice in subjectAreasForCreating" :key="choice" :value="choice">
          {{choice}}
        </option>
      </select>
  </div>

  <div class="d-flex justify-content-center">
    <button class="btn btn-success">Create Subject</button>
  </div>
  <span class="text-center error" v-if="errorMessage">{{ errorMessage }}</span>
</div>
  </form>
</div>
  </div>

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
              <div class="alert alert-primary">
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

<div class="d-flex justify-content-center">
  <button class="btn btn-dark mb-3" style="background-color: var(--dark-green);" data-bs-toggle="collapse" data-bs-target="#debateCollapse">
    Show/Hide Debating Area for {{subject.name }} ({{subject.subject_code}})
  </button>
</div>

<div class="alert alert-success collapse" id="debateCollapse">
  <div class="row">
    <div class="">
      <div v-for="area in debatingAreas" :key="area.id">
        <div v-if="area.related_subject === subject.id">
          <h3 class="text-center mb-4">{{ area.name }}</h3>
          <h1 class="text-center mb-4"><strong>Debate question: </strong>{{ area.debate_question }}</h1>
      <div class="card mt-3 p-3 mx-auto" style="width:40vw;">
        <div v-if="currentUserRole == 'Teacher'">
          <h5 class="text-center mb-4 text-muted">Pesonal Target Contribution: Students will see a target based on their CD values (see 'Manage Teaching')</h5>
        <div class="card alert alert-warning">Here will be a progress bar showing how far away they are for each subject!</div>        
        </div>
        <div v-if="currentUserRole == 'Student'" class="progress">
  <div class="progress-bar bg-success" role="progressbar" aria-label="Success example" style="width: 65%" aria-valuenow="65" aria-valuemin="0" aria-valuemax="100"></div>
</div>        
      </div>
          <h4 class="mt-3 text-center mb-4">Sides:</h4>
          <div class="d-flex justify-content-center">
          <div class="card mt-3 p-3" style="width: 60vw;">
  <div v-for="side in area.sides" :key="side.id">
    <div class="card mt-3 p-3">
      <h5>{{ side.side_name }}</h5>
      <p><strong>Opinions:</strong></p>
      <ul>
        <li v-for="opinion in side.opinions" :key="opinion.id">
          {{ opinion.text }} ({{ opinion.thumbs_up }} thumbs up, {{ opinion.thumbs_down }} thumbs down)
        </li>
        <li v-if="side.opinions.length === 0">No opinion has been added to this side yet!</li>
      </ul>
    </div>
  </div>
</div>
</div>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="d-flex justify-content-center">
  <button class="btn btn-dark mt-3" style="background-color: var(--dark-gray);" data-bs-toggle="collapse" data-bs-target="#collapseExample" @click="toggleCommunicationArea">
    {{ communicationArea.showCommunicationArea ? 'Hide Communication Area' : 'Show Communication Area' }} for {{subject.name}} ({{subject.subject_code}})
  </button>
</div>


<!-- communication area channels -->

<div class="collapse" id="collapseExample">
  <div class="card card-body mt-3" style="outline: none;">
        <div class="row ms-1">
  <div class="col-4 rounded scrollable-g" style="height: 45vh; background-color: var(--dark-purple);">
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
      <div  class="scrollable-g mt-3" style="height: 40vh;">
        <div v-if="communicationArea.displayChannelClicked && communicationArea.currentChannelPosts.length === 0">
          This channel has no content, feel free to add! </div><div v-else><div v-if="communicationArea.currentChannelPosts.length === 0">Browse one of the channels on the left hand side</div>
</div>
      <div v-for="post in communicationArea.currentChannelPosts">
      <div class="alert alert-secondary mx-2">
        <div class="d-flex">
          <div v-for="user in users">
    <img v-if="post.author_username == user.username" class="img rounded mx-2" style="width: 4vw" :src="'http://127.0.0.1:8000'+ user.profile_image_url">
  </div>

          <div>
            <h6 class="p-2">{{post.author_username}} ({{ post.author_role }}) <span class="text-muted p-1"> - {{timeElapsed(post.created_at)}}</span></h6>
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
        errorMessage:'',
        currentUser:'',
        currentUserRole:'',
        users: [],
        subjectAreas: [],
        subjects: [],
        filteredSubjects: [],
        currentSubjectArea: '',
        communicationArea: {
          showCommunicationArea: false,
          communicationAreas:[],
          communicationChannels:[],
          currentChannelName:'',
          currentChannelPosts:[],
          displayChannelClicked: false,
          currentChannelID: null,
          currentChannel: [],
          channelPost:''
        },
        createSubject: {
        subjectchoice:'',
        categorychoice:'', yearchoice:'',
        subjectAreasForCreating:[]
        },
        subjectChoices:[],
        yearChoices:[],
        debatingAreas:[],
        debatingSides:[],
        debatingOpinions:[]
      }
    },
    async mounted() {
      await axios.get('api/v1/LP/getCustomUsers/').then(response => {
      this.users = response.data
    })
  
      await axios.get('/api/v1/LP').then(response => {
        this.subjects = response.data
        this.filteredSubjects = this.subjects
      })

      await axios.get('/api/v1/LP/getCommunicationAreas/').then(response => {
        this.communicationArea.communicationAreas = response.data
      })

      await axios.get('/api/v1/LP/getCommunicationChannels/').then(response => {
        this.communicationArea.communicationChannels = response.data
        
      })
      
      await axios.get('/api/v1/LP/getDebatingAreas/').then(response => {
        const { debating_areas, debate_sides, opinions } = response.data;
        this.debatingAreas = debating_areas;
        this.debatingSides = debate_sides;
        this.debatingOpinions = opinions;
        });
      
    },
    created(){
      axios.get('api/v1/LP/subjectCategories/').then(response => {
          this.subjectAreas = response.data;
          this.subjectAreasForCreating = response.data[0].CATEGORY_CHOICES.map(choice => choice[0]).flat();
      });

      axios.get('/api/v1/LP/getCurrentUser/').then(response => {
        this.currentUser = response.data.username
        this.currentUserRole = response.data.role
      });

      axios.get('/api/v1/LP/getGeneralSubjectInformation/').then(response => {
      const choices = response.data;
      this.subjectChoices = Object.fromEntries(Object.entries(choices.subject_choices).map(([key, value]) => [key, value]));
      this.yearChoices = Object.fromEntries(Object.entries(choices.year_choices).map(([key, value]) => [key, value]));
      });
    },
    methods: {  
      async createSubjectForOverview(){
       if (this.createSubject.subjectchoice
       && this.createSubject.categorychoice && this.createSubject.yearchoice){
            await axios.post('api/v1/LP/createSubject/', this.createSubject)
            .then(response => {
            }).catch(error =>{
                if(error.response){
                    for (const property in error.response.data){
                        this.errors.push(`${property}: ${error.response.data[property]}`)
                    }
                }
            })
            this.errorMessage = '';

            } else {
                this.errorMessage = 'All four fields are required';
              }

          await axios.get('/api/v1/LP').then(response => {
           this.subjects = response.data
           this.filteredSubjects = this.subjects
           })

          alert("Subject has been created")
      },

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
    toggleCommunicationArea() {
      this.communicationArea.showCommunicationArea = !this.communicationArea.showCommunicationArea;
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
    --dark-green: rgb(0, 158, 13);
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