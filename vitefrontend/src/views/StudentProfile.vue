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
      showAlert: false
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
        this.currentEngagementType = response.data.desired_engagement_type
        this.EngagementChoices = response.data.ENG_TYPES.map(choice => choice[1])
      })

    },
    computed: {
    submitButtonDisabled() {
      return this.selectedEngagementType === ''
    },
  },
  watch: {
    selectedEngagementType(newValue, oldValue) {
      if (this.showAlert) {
        this.showAlert = false
      }}}
  }
</script>