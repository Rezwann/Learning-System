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
    <h4 class="alert-heading">EHCP</h4>

    <div v-if="hasEHCP===true">
    <div v-for="(ehcpInfo, index) in allInformationEHCP" :key="index">
      <h4 class="alert-heading">Section {{ index + 1 }} - {{ Object.keys(ehcpInfo)[index].toUpperCase().replace('_', ' ') }}</h4>
  <h5 class="card-subtitle text-muted mt-2">{{ ehcpInfo.student_views }}</h5>
  <h5 class="card-subtitle text-muted mt-2">{{ ehcpInfo.student_interests }}</h5>
  <h5 class="card-subtitle text-muted mt-2">{{ ehcpInfo.student_aspirations }}</h5>
  <h5 class="alert alert-success mt-3">
    {{ ehcpInfo.teacher_comments.length > 0 ? ehcpInfo.teacher_comments : 'No teacher comments' }}
  </h5>
</div></div>

<div v-else>{{currentUser}}, you do not have a EHCP. You may need to speak to a teacher about this.</div>
</div>

    </div>
  </div>
</template>

<script>
import axios from 'axios'

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