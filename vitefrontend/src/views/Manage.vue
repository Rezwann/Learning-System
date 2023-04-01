<template>
    <div class="container-md">
      <div class="mb-4"></div>
    <div><h1 class="text-center mb-4">Manage Teaching</h1></div>
    <div class="alert alert-danger" role="alert">

  <h4 class="alert-heading">Search for a student</h4>
  <div class="row">
  <div class="col-8 mb-3">
    <select v-model="selectedStudent" class="form-control mt-3">
      <option value="">-- Select a student --</option>
      <option v-for="student in filtered" :value="student.username">{{ student.username }} ({{student.role}} ID: {{student.id}})</option>
    </select>
  </div>
</div>

<div v-if="selectedStudent">
  <h2>{{selectedStudent}}'s Cognitive Domains Levels (observational)</h2>      
  <canvas class="container-sm" id="myChart"></canvas>
</div>
  <hr>
      <h4 class="alert-heading">Manage Subject Content</h4>
  <p>
  </p>
  <hr>
  <h4 class="alert-heading">Add to Student's Individual Learning Workspace</h4>
  <p>.</p>
  <hr>


</div>
</div>
</template>

<script>
import Chart from 'chart.js/auto';
import axios from 'axios';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const CDs = [           
      "Verbal Memory", "Non Verbal Memory", "Visual Perception",
      "Visual Information Processing Speed", "Numeracy", "Literacy", 
      "Executive Function", "Verbal Reasoning"]

export default {
  name: 'Manage',
  components: { Bar },
  data() {
    return {
      currentUser:'',    
      students: [],
      filtered:[],
      selectedStudent: '',
      selectedStudentNeuroBackground:[],
      CognitiveValues: {
        VB:0,
        NVM:0,
        VP:0,
        VIPS:0,
        N:0,
        L:0,
        EF:0,
        VR:0
      },
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
    async GenerateNeuroInsight() { 

      if (!this.selectedStudent) {
        return;
      }

      await axios.post('/api/v1/LP/getUserNeurobackground/', {studentname:this.selectedStudent})
          .then(response => {
            this.selectedStudentNeuroBackground = response.data
            'verbal_memory_level'
                  ,'non_verbal_memory_level', 'visual_perception_level',
                  'visual_information_processing_speed_level',
                  'numeracy_level', 'literacy_level', 'executive_function_level',
                  'verbal_reasoning_level'


          })   

          const ctx = document.getElementById('myChart')

const myChart = new Chart(ctx, {
type: 'bar',
data: {
    labels: CDs,
    datasets: [{
        label: 'Level',
        data: [this.selectedStudentNeuroBackground.verbal_memory_level,
        this.selectedStudentNeuroBackground.non_verbal_memory_level,
        this.selectedStudentNeuroBackground.visual_perception_level,
        this.selectedStudentNeuroBackground.visual_information_processing_speed_level,
        this.selectedStudentNeuroBackground.numeracy_level,
        this.selectedStudentNeuroBackground.literacy_level,
        this.selectedStudentNeuroBackground.executive_function_level,
        this.selectedStudentNeuroBackground.verbal_reasoning_level],
        borderWidth: 1
    }],
},
options: {
  indexAxis: 'y',
  elements: {
  bar: {
    borderWidth: 1,
  },
},
plugins: {
  title: {
      display: true,
    },
  legend: {
    position: 'right',
  },},

  scales: {
  x: {
    min: 0,
    max: 100,
    ticks: {
      stepSize: 10,
      callback: function(value) {
        if (value === 50) {
          return '50 (center)';
        }
        return value;
      }
    }
  },
  y: {
    beginAtZero: false
  }
},
responsive:false,
}
});
    },    
}
}
</script>  
