<template>
    <div class="container-xxl">
      <div class="mb-4"></div>
    <div><h1 class="text-center mb-4">Manage Teaching</h1></div>
    <div class="alert alert-danger">
      <div class="row">
  <div class="col-md-4">
    <h4 class="alert-heading">Search for a student</h4>
  </div>
  <div class="col-md-9 mb-3">
    <div class="d-flex">
      <select v-model="selectedStudent" class="form-control flex-grow-1">
        <option value="">-- Select a student --</option>
        <option v-for="student in filtered" :value="student.username">{{ student.username }} ({{student.role}} ID: {{student.id}})</option>
      </select>
      <button @click="resetSelectedStudent" class="btn btn-secondary ms-3">Clear</button>
    </div>
  </div>  
</div>

<div v-if="selectedStudent" class="row">
  <div class="col-md-6">
    <h4>{{selectedStudent}}'s Cognitive Domains Levels</h4>          
    <div class="container-md card p-3">
      <apexchart type="bar" :options="options" :series="series" height="350" />
      <h5>Impact on Learning Activity Fragments:</h5>
      <h6>Learning Activity Debate Total Contribution Target (CDs considered): {{selectedStudentDebateTarget}}</h6>
      <h6>Learning Activity Vocabulary Sheet Group (CDs considered): {{selectedStudentVocabularyGroup}}</h6>
    </div>
  </div>
  <div class="col-md-6">
    <h4>Update {{selectedStudent}}'s Levels</h4>
    <div id="updatingcogvalues" class="card p-3">
      <p>{{CDs[0]}}: {{selectedVM}}</p>   
      <input type="range" class="form-range" min="1" max="100" step="1" v-model="selectedVM">
      <p>{{CDs[1]}}: {{selectedNVM}}</p> 
      <input type="range" class="form-range" min="1" max="100" step="1" v-model="selectedNVM">
      <p>{{CDs[2]}}: {{selectedVP}}</p> 
      <input type="range" class="form-range" min="1" max="100" step="1" v-model="selectedVP">
      <p>{{CDs[3]}}: {{selectedVIPS}}</p> 
      <input type="range" class="form-range" min="1" max="100" step="1" v-model="selectedVIPS">
      <p>{{CDs[4]}}: {{selectedN}}</p> 
      <input type="range" class="form-range" min="1" max="100" step="1" v-model="selectedN">
      <p>{{CDs[5]}}: {{selectedL}}</p> 
      <input type="range" class="form-range" min="1" max="100" step="1" v-model="selectedL">
      <p>{{CDs[6]}}: {{selectedEF}}</p> 
      <input type="range" class="form-range" min="1" max="100" step="1" v-model="selectedEF">
      <p>{{CDs[7]}}: {{selectedVR}}</p> 
      <input type="range" class="form-range" min="1" max="100" step="1" v-model="selectedVR">
      <button @click="updateStudentNeuroBackground" class="btn btn-danger mt-3">Update Levels</button>
    </div>
  </div>
  <div class="card mt-3 p-3 mx-auto" style="width:80vw;">
  <h4>{{selectedStudent}}'s Desired Engagement Type</h4>
  <div class="d-flex flex-wrap align-items-center">
  <h5 class="card-title">{{selectedStudent}}'s Currently Set Desired Engagement Type:&nbsp;</h5>
  <h5 class="card-subtitle text-muted"> {{selectedStudentCurrentEngagementType}}</h5>
</div>
  <h5 class="card-title">{{selectedStudent}}'s Desired Engagement Type History:</h5>
  <div class="card shadow-sm alert alert-success mt-2">
        <div class="scrollable-b">
          <div v-if="selectedStudentEngagementInstances.length === 0">
  <h4 class="justify-content-center">{{selectedStudent}} has not previously set an engagement preference</h4>
</div>
  <div v-for="instance in selectedStudentEngagementInstances" :key="instance.id">
    <div class="mx-3">
      <div class="col-12 row mt-2">
          <div class="card shadow-xxl alert alert-warning" style="height: 8vh;">
    <p>Chosen Type: {{ instance.chosen_type }} | Time Chosen: {{timeElapsed(instance.time_chosen)}}</p></div>
</div>      </div>
</div>
  </div>
</div>
<h5 class="card-title">{{selectedStudent}}'s Desired Engagement Type Visualisation:</h5>
<div v-if="selectedStudentEngagementInstances.length >= 5">
  <apexchart type="area" :options="optionsEngagement" :series="seriesEngagement" height="350"/>
</div>
<div v-else>
  <h6 class="card-subtitle text-muted">Not enough instances. Once {{selectedStudent}} has selected their preference for engagement type at least 5 times, you will be able to see their preference in a visualization below</h6>
</div>
  </div>

  <div class="card mt-3 p-3 mx-auto" style="width:80vw;">
  <h4 class="alert-heading mt-2">Add to {{selectedStudent}}'s Individual Workspace</h4>

  <form @submit.prevent="submitNewBoard">
    <div class="row">
  <h5 class="card-text">Add a board (for example, a task)</h5>
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
    <button class="btn btn-danger">Add Board</button>
  </div>
  <span class="text-center error" v-if="errorMessage">{{ errorMessage }}</span>
</div>
  </form>
</div>

<div class="card mt-3 p-3 mx-auto" style="width:80vw;">
  <h4 class="alert-heading mt-2">EHCP</h4>
<div v-bind="!selectedStudentHasEHCP == true">  

  <div v-for="(ehcpInfo, index) in allSelectedStudentInformationEHCP" :key="index">
      <h4 class="alert-heading">Section {{ index + 1 }} - {{ Object.keys(ehcpInfo)[index].toUpperCase().replace('_', ' ') }}</h4>
  <h5 class="card-subtitle text-muted mt-2">{{ ehcpInfo.student_views }}</h5>
  <h5 class="card-subtitle text-muted mt-2">{{ ehcpInfo.student_interests }}</h5>
  <h5 class="card-subtitle text-muted mt-2">{{ ehcpInfo.student_aspirations }}</h5>
  <h5 class="alert alert-success mt-3">
    {{ ehcpInfo.teacher_comments.length > 0 ? ehcpInfo.teacher_comments : 'No teacher comments' }}
  </h5>
</div>


  <h6 class="card-subtitle text-muted">You can fill in the form below to setup or update {{selectedStudent}}'s EHCP information. This will appear in {{selectedStudent}}'s profile once completed.'</h6>  
</div>

<form @submit.prevent="setupEHCP();">
    <div class="row">
  <div class="col-4 mb-3">
    <label class="mb-1">Set EHCP Views ({{selectedStudent}}'s views)</label>
    <input type="text" name="EHCPview" class="form-control" v-model="setEHCPview" placeholder="Enter views of the student here">
  </div>
  <div class="col-4 mb-3">
    <label class="mb-1">Set EHCP Interests ({{selectedStudent}}'s interests)</label>
    <input
      type="text"
      name="short_description"
      class="form-control"
      v-model="setEHCPinterest" placeholder="Enter interests of the student here"
    />
  </div>
  <div class="col-4 mb-3">
    <label class="mb-1">Set EHCP Aspirations ({{selectedStudent}}'s aspirations)</label>
    <input
      type="text"
      name="short_description"
      class="form-control"
      v-model="setEHCPaspiration" placeholder="Enter aspirations of the student here"
    />
  </div>
  <div class="col-4 mt-4 mb-3">
    <button class="btn btn-warning">Setup/Update {{selectedStudent}}'s EHCP</button>
  </div>
  <span class="text-center error" v-if="errorMessage">{{ errorMessage }}</span>
</div>
  </form>

</div>

</div>

</div>
</div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts';
import axios from 'axios';
import moment from 'moment';

const CDs = [           
      "Verbal Memory", "Non Verbal Memory", "Visual Perception",
      "Visual Information Processing Speed", "Numeracy", "Literacy", 
      "Executive Function", "Verbal Reasoning"]

export default {
  name: 'Manage',
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      errorMessage:'',
      currentUser:'',    
      students: [],
      filtered:[],
      selectedStudent: '',
      selectedStudentList: [],
      selectedStudentNeuroBackground:[],
      selectedID:0,
      selectedVM:0, selectedNVM: 0, selectedVP:0, selectedVIPS: 0,
      selectedN:0, selectedL: 0, selectedEF: 0, selectedVR: 0,
      selectedStudentDebateTarget: 0,
      selectedStudentVocabularyGroup:'',
      selectedStudentHasEHCP: false,
      CDs: CDs,
      options:{},
      series:[],
      EngagementChoices:[],
      selectedStudentCurrentEngagementType:'',
      EngagementInstances:[],
      selectedStudentEngagementInstances:[],
      optionsEngagement:{},
      seriesEngagement:[],
      enoughInstances: false,
      engagementCounts:[],
      addBoardForm: {
            name:'',
            short_description:''
        },
      errorMessage:'',
      setEHCPview:'',
      setEHCPinterest:'',
      setEHCPaspiration:'',
      allSelectedStudentInformationEHCP:[],
      showEHCP: false
    }
  },
  async mounted() {  
    await axios.get('/api/v1/LP/getCurrentUser/').then(response => {
      this.currentUser = response.data.username
    })
    
  },
  created(){
    axios.get('/api/v1/LP/getCurrentUser/').then(response => {
      this.currentUser = response.data.username
    })

    axios.get('/api/v1/LP/getCustomUsers/').then(response => {
      this.students = response.data
      this.filtered = this.students.filter(student => student.role === 'Student');
    })    

    axios.get('/api/v1/LP/getSingleUser/').then(response => {
        this.EngagementChoices = response.data.ENG_TYPES.map(choice => choice[1])
      })    
  },
  watch: {
    selectedStudent: {
      handler: 'GenerateNeuroInsight',
      immediate: true,      
    },
    selectedStudentEngagementInstances: function(newVal) {
      if (newVal.length >= 5) {
        this.enoughInstances = true;
        this.showEngagementVisualisation();
      } else {
        this.enoughInstances = false;
      }
    }
  },
  methods: {   
    async setupEHCP(){
            if (this.setEHCPinterest && this.setEHCPaspiration && this.setEHCPview){
            await axios.post('api/v1/LP/setEHCP/', 
            
            {studentname:this.selectedStudent, ehcpInterest: this.setEHCPinterest,
              ehcpAspiration: this.setEHCPaspiration, ehcpView: this.setEHCPview            
            })
            .then(response => {
            }).catch(error =>{
                if(error.response){
                    for (const property in error.response.data){
                        this.errors.push(`${property}: ${error.response.data[property]}`)
                    }
                }
            })
            this.errorMessage = '';
            this.setEHCPinterest = ''
            this.setEHCPaspiration = ''
            this.setEHCPview = ''
            } else {
                this.errorMessage = 'All three EHCP fields are required';
              }
        },

    timeElapsed(created_at) {
            const currentDate = moment()
            const createdAt = moment(created_at)
            const date = createdAt.format('MMM D, YYYY [at] h:mm A')
            const elapsed = moment.duration(currentDate.diff(createdAt)).humanize()
                    return `${date} (${elapsed} ago)`
        },
        
        async submitNewBoard(){
            if (this.addBoardForm.name && this.addBoardForm.short_description){
            await axios.post('api/v1/LP/addLearningBoardToStudent/',{boardinfo: this.addBoardForm, studentname:this.selectedStudent})
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
            alert("Board added")
            } else {
                this.errorMessage = 'Both fields are required';
              }
        },
    async showEngagementVisualisation(){
          this.optionsEngagement = {
        chart: { type: 'area',
    stacked: true,    
    toolbar: {
      show: false
    },
  },
  title: {
    text: this.selectedStudent,
    align: 'center'
  },

  dataLabels: {
    enabled: false
  },
  xaxis: {
    categories: this.EngagementChoices, 
    labels: {
  }   
  },
      };

      this.seriesEngagement = [
        {
          name: 'Count',
          data: [this.selectedStudentEngagementInstances.filter(item => item.chosen_type === this.EngagementChoices[0]).length,
      this.selectedStudentEngagementInstances.filter(item => item.chosen_type === this.EngagementChoices[1]).length,
      this.selectedStudentEngagementInstances.filter(item => item.chosen_type === this.EngagementChoices[2]).length,
      this.selectedStudentEngagementInstances.filter(item => item.chosen_type === this.EngagementChoices[3]).length,
      this.selectedStudentEngagementInstances.filter(item => item.chosen_type === this.EngagementChoices[4]).length,
      this.selectedStudentEngagementInstances.filter(item => item.chosen_type === this.EngagementChoices[5]).length
]
        }
      ];
    },

    async updateStudentNeuroBackground(){
      await axios.post('api/v1/LP/updateStudentNeuroBackground/', {studentname:this.selectedStudent, VM:this.selectedVM, NVM:this.selectedNVM,
      VP: this.selectedVP, VIPS: this.selectedVIPS, N: this.selectedN, 
      L: this.selectedL, EF: this.selectedEF, VR: this.selectedVR, DEBATE_TARGET: this.selectedStudentDebateTarget, VG: this.selectedStudentVocabularyGroup })
          .then(response => {
          })
          const studentName = this.selectedStudent

          await this.resetSelectedStudent();
          await this.chooseSelectedStudent(studentName)
          await this.showEngagementVisualisation()
          await this.getStudentEHCP()
    },
    
    async resetSelectedStudent() {
    this.selectedStudent = ''
    },
    async chooseSelectedStudent(name){
      this.selectedStudent = name
    },
    async GenerateNeuroInsight(option = 'default') {       
      if (option = 'default'){
      await axios.post('/api/v1/LP/getUserNeurobackground/', {studentname:this.selectedStudent})
          .then(response => {
            this.selectedStudentNeuroBackground = response.data
            this.selectedVM = this.selectedStudentNeuroBackground.verbal_memory_level
            this.selectedNVM = this.selectedStudentNeuroBackground.non_verbal_memory_level
            this.selectedVP = this.selectedStudentNeuroBackground.visual_perception_level
            this.selectedVIPS = this.selectedStudentNeuroBackground.visual_information_processing_speed_level
            this.selectedN = this.selectedStudentNeuroBackground.numeracy_level
            this.selectedL = this.selectedStudentNeuroBackground.literacy_level
            this.selectedEF = this.selectedStudentNeuroBackground.executive_function_level
            this.selectedVR = this.selectedStudentNeuroBackground.verbal_reasoning_level            
            this.selectedStudentDebateTarget = this.selectedStudentNeuroBackground.debate_contribution_target
            this.selectedStudentVocabularyGroup = this.selectedStudentNeuroBackground.vocabulary_sheet_group            
            this.selectedStudentCurrentEngagementType = this.selectedStudentNeuroBackground.desired_engagement_type 
            this.selectedStudentHasEHCP = this.selectedStudentNeuroBackground.hasEHCP 

          })  

          await axios.get('/api/v1/LP/getEngagementInstances/').then(response => {
  this.EngagementInstances = response.data;
  this.selectedStudentEngagementInstances = this.EngagementInstances
    .filter(instance => instance.username === this.selectedStudent)
    .map(instance => ({
      id: instance.id,
      username: instance.username,
      chosen_type: instance.chosen_type,
      time_chosen: instance.time_chosen
    }))
    .sort((a, b) => new Date(b.time_chosen) - new Date(a.time_chosen));
});

          await axios.post('/api/v1/LP/getStudentEHCP/',{name:this.selectedStudent}).then(response => {
            this.allSelectedStudentInformationEHCP = Object.values(response.data).map(ehcp => {
        return {
        student_views: ehcp.student_views,
        student_interests: ehcp.student_interests,
        student_aspirations: ehcp.student_aspirations,
        teacher_comments: ehcp.teacher_comments
        };
        });
      });

        }        
        else {
          await axios.post('/api/v1/LP/getUserNeurobackground/', {studentname:option})
          .then(response => {
            this.selectedStudentNeuroBackground = response.data
            this.selectedID = this.this.selectedStudentNeuroBackground.id
            this.selectedVM = this.selectedStudentNeuroBackground.verbal_memory_level
            this.selectedNVM = this.selectedStudentNeuroBackground.non_verbal_memory_level
            this.selectedVP = this.selectedStudentNeuroBackground.visual_perception_level
            this.selectedVIPS = this.selectedStudentNeuroBackground.visual_information_processing_speed_level
            this.selectedN = this.selectedStudentNeuroBackground.numeracy_level
            this.selectedL = this.selectedStudentNeuroBackground.literacy_level
            this.selectedEF = this.selectedStudentNeuroBackground.executive_function_level
            this.selectedVR = this.selectedStudentNeuroBackground.verbal_reasoning_level            
            this.selectedStudentDebateTarget = this.selectedStudentNeuroBackground.debate_contribution_target
            this.selectedStudentCurrentEngagementType = this.selectedStudentNeuroBackground.desired_engagement_type
          })

          await axios.get('/api/v1/LP/getEngagementInstances/').then(response => {
            this.EngagementInstances = response.data;
            this.selectedStudentEngagementInstances = this.EngagementInstances
            .filter(instance => instance.username === this.selectedStudent)
            .map(instance => ({
            id: instance.id,
            username: instance.username,
            chosen_type: instance.chosen_type,
            time_chosen: instance.time_chosen
            }));
          });

          await axios.post('/api/v1/LP/getStudentEHCP/',{name:option}).then(response => {
            this.allSelectedStudentInformationEHCP = Object.values(response.data).map(ehcp => {
        return {
        student_views: ehcp.student_views,
        student_interests: ehcp.student_interests,
        student_aspirations: ehcp.student_aspirations,
        teacher_comments: ehcp.teacher_comments
        };
        });
      });

        }
      this.options = {
        chart: {
    type: 'bar',
    height: 450,
    stacked: true,    
    toolbar: {
      show: false
    },
  },
  title: {
    text: this.selectedStudent,
    align: 'center'
  },
  plotOptions: {
    bar: {
      horizontal: true,
    },
  },
  dataLabels: {
    enabled: false
  },
  xaxis: {
    categories: CDs,
  },
      };

      this.series = [
        {
          name: 'Level',
          data: [this.selectedVM,
          this.selectedNVM,
          this.selectedVP,
          this.selectedVIPS,
          this.selectedN,
          this.selectedL,
          this.selectedEF,
          this.selectedVR]
        }
      ];
        },    
        }
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