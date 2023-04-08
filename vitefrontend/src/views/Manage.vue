<template>
    <div class="container-xxl">
      <div class="mb-4"></div>
    <div><h1 class="text-center mb-4">Manage Teaching</h1></div>
    <div class="alert alert-danger" role="alert">

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
</div>

  <hr>
  <h4 class="alert-heading">Add to Student's Individual Learning Workspace</h4>
  <p>.</p>
  <hr>

</div>
</div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts'
import axios from 'axios';

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
      currentUser:'',    
      students: [],
      filtered:[],
      selectedStudent: '',
      selectedStudentList: [],
      selectedStudentNeuroBackground:[],
      selectedVM:0, selectedNVM: 0, selectedVP:0, selectedVIPS: 0,
      selectedN:0, selectedL: 0, selectedEF: 0, selectedVR: 0,
      selectedStudentDebateTarget: 0,
      selectedStudentVocabularyGroup:'',
      CDs: CDs,
      options:{},
      series:[]
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
  },
  watch: {
    selectedStudent: {
      handler: 'GenerateNeuroInsight',
      immediate: true,
    },
  },
  methods: {   
    async updateStudentNeuroBackground(){
      await axios.post('api/v1/LP/updateStudentNeuroBackground/', {studentname:this.selectedStudent, VM:this.selectedVM, NVM:this.selectedNVM,
      VP: this.selectedVP, VIPS: this.selectedVIPS, N: this.selectedN, 
      L: this.selectedL, EF: this.selectedEF, VR: this.selectedVR, DEBATE_TARGET: this.selectedStudentDebateTarget, VG: this.selectedStudentVocabularyGroup })
          .then(response => {
          })
          const studentName = this.selectedStudent
          await this.resetSelectedStudent();
          await this.chooseSelectedStudent(studentName)
    },
    async resetSelectedStudent() {
    this.selectedStudent = ''
    },
    async chooseSelectedStudent(name){
      this.selectedStudent = name
    },
    async GenerateNeuroInsight(option = 'default') { 
      console.log(this.selectedStudentList)
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

          })   
        }
        else {
          await axios.post('/api/v1/LP/getUserNeurobackground/', {studentname:option})
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
          })   
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
</style>