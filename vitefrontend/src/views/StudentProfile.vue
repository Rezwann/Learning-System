<template>
  <div class="container-md">
    <div class="mb-4"></div>
    <div>
      <h1 class="text-center">Profile</h1>
    </div>
    <div class="alert alert-warning" role="alert">
      <div class="row">
        <h4 class="alert-heading">Select a desired engagement type</h4>
        <h5>
          <span>Currently set to: </span
          ><span v-bind:textContent="currentEngagementType"></span>
        </h5>
        <select
        v-model="selectedEngagementType"
        class="form-select form-select-lg mb-3"
        aria-label=".form-select-lg"
      >
        <option selected disabled value="">Select engagement type</option>
        <option v-for="choice in EngagementChoices" :key="choice" :value="choice">
          {{ choice }}
        </option>
      </select>
      </div>
      <div class="d-flex justify-content-center">
        <button
          @click="submitNewEngagementInstance"
          class="btn btn-primary"
          :disabled="submitButtonDisabled"
        >
          Set type
        </button>
      </div>
      <div class="alert alert-primary mt-3" v-show="showAlert">
      Your engagement type has been updated. This will be reflected in the profile information your teacher has access to.
      <button type="button" class="p-2 btn-close" @click="showAlert = false"></button>
    </div>
    <div class="container-md mt-3 card p-3">
    <h4 class="alert-heading">Your EHCP</h4>

    <div v-if="hasEHCP===true">
      <div v-for="(ehcpInfo, index) in allInformationEHCP" :key="index">
  <h4 class="alert-heading">Section {{ index + 1 }} - {{ Object.keys(ehcpInfo)[index].toUpperCase().replace('_', ' ') }}</h4>
  <h5 class="card-subtitle text-muted mt-2">{{ ehcpInfo.student_views }}</h5>
  <h5 class="card-subtitle text-muted mt-2">{{ ehcpInfo.student_interests }}</h5>
  <h5 class="card-subtitle text-muted mt-2">{{ ehcpInfo.student_aspirations }}</h5>
  <div class="card shadow-sm alert alert-success mt-2">
        <div class="scrollable-b">
  <div v-if="ehcpInfo.teacher_comments.length > 0">
    <div v-for="(comment, i) in ehcpInfo.teacher_comments" :key="i">
      <h5 class="alert alert-primary card mt-2">
        <strong>{{ comment.user }} (Teacher):</strong> {{ comment.comment }}<small class="text-muted mt-2">{{ timeElapsed(comment.created_at) }}</small>
      </h5>
    </div>
  </div>
  <h5 class="alert alert-warning mt-3" v-else>No teacher comments</h5>
</div>
</div></div>
    </div>
<div v-else>{{currentUser}}, you do not have a EHCP. You may need to speak to a teacher about this.</div>
</div>




    </div>
  </div>
</template>

<script>
import axios from 'axios'
import moment from 'moment'

export default {
  name: 'StudentProfile',
  data() {
    return {
      currentUser: '',
      currentUserRole: '',
      currentEngagementType:'',
      EngagementChoices:[],
      selectedEngagementType:'',
      isLoading: true,
      showAlert: false,
      hasEHCP:false,
      allInformationEHCP: []
    }
  },
  methods:{
    timeElapsed(created_at) {
            const currentDate = moment()
            const createdAt = moment(created_at)
            const date = createdAt.format('MMM D, YYYY [at] h:mm A')
            const elapsed = moment.duration(currentDate.diff(createdAt)).humanize()
                    return `${date} (${elapsed} ago)`
        },
    async submitNewEngagementInstance(){
    await axios.post('/api/v1/LP/postEngagementInstance/', {chosentype:this.selectedEngagementType}).then(response => {        
      this.showAlert = true;
    })

    await axios.get('/api/v1/LP/getSingleUser/').then(response => {
        this.currentEngagementType = response.data.desired_engagement_type
        this.EngagementChoices = response.data.ENG_TYPES.map(choice => choice[1])
      })
    },
  },
  created(){
    axios.get('/api/v1/LP/getSingleUser/').then(response => {
      this.currentUser = response.data.username
      this.hasEHCP = response.data.hasEHCP
      this.currentEngagementType = response.data.desired_engagement_type
        this.EngagementChoices = response.data.ENG_TYPES.map(choice => choice[1])
      })
      axios.get('/api/v1/LP/getAllEHCP/').then(response => {
        this.allInformationEHCP = Object.values(response.data).map(ehcp => {
          return {
        student_views: ehcp.student_views,
        student_interests: ehcp.student_interests,
        student_aspirations: ehcp.student_aspirations,
        teacher_comments: ehcp.teacher_comments
        };
        });
      });

    },
    computed: {
    submitButtonDisabled() {
      return this.selectedEngagementType === ''
    },
  },
  watch: {
    selectedEngagementType() {
      if (this.showAlert) {
        this.showAlert = false
      }}}
  }
</script>

<style>
  .scrollable-b {
  overflow-y: scroll;
  max-height: 20vh; 
}

.scrollable-b::-webkit-scrollbar {
    border-radius: 10rem;
    background-color: #f1f1f19a;
    width: 0.75rem;
}

.scrollable-b::-webkit-scrollbar-thumb {
  border-radius: 1rem;
  margin: 1rem;
  width: 0.75rem;
  background-color: rgb(0, 74, 158);
}

.scrollable-b::-webkit-scrollbar-thumb:hover {
  border-radius: 1rem;
  margin: 1rem;
  width: 0.75rem;
  background-color: rgb(2, 108, 222);
}

</style>