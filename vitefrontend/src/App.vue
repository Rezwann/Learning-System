<template>
  <div class="" v-bind:style="{ filter: 'saturate(' + saturation + '%)' }">
    <div v-bind:key="font" v-bind:style="{ fontFamily: font}">
    <div class="navbar navbar-expand navbar-light bg-indigo-800">
      <h4 class="mx-4 mt-2 text-white me-auto">Rezwan: Learning Platform 🙂</h4>
            <div class="navbar-nav ml-auto mx-4 mb-1 mt-1">              
              <button class="btn btn-success nav-item nav-link text-white mx-2" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasExample" aria-controls="offcanvasExample">Accessibility</button>
              <button type="button" class="btn btn-success nav-item nav-link text-white mx-2" data-bs-toggle="modal" data-bs-target="#exampleModal">
          View Key Dates
          </button>

          <button
          class="nav-item nav-link btn btn-light mx-2 "
          @click="$router.push('/')"
        >
          Home
        </button>
        <template v-if="$store.state.isAuthenticated">
          <button
            class="nav-item nav-link btn btn-light mx-2"
            @click="$router.push('/overview')"
          >
            Overview
          </button>
          <template v-if="currentUserRole === 'Student'">
          <button
          class="nav-item nav-link btn btn-light mx-2"
          @click="$router.push('/studentprofile')"
        >
          Student Profile
        </button></template>
          <button
            class="nav-item nav-link btn btn-light mx-2"
            @click="$router.push('/workspace')"
          >
            Learning Workspace
          </button>
          <template v-if="currentUserRole === 'Teacher'">
            <button 
            class="nav-item nav-link btn btn-light mx-2"
              @click="$router.push('/manage')"
            >
              Manage Teaching
            </button>
          </template>
          <button
            class="nav-item nav-link text-white btn btn-danger mx-2"
            @click="$router.push('/logout')">Logout
          </button>
        </template>
        <template v-else>
        <button
            class="nav-item nav-link btn btn-warning mx-2"
            @click="$router.push('/register')"
          >
            Register
          </button>
          <button
            class="nav-item nav-link btn btn-warning mx-2"
            @click="$router.push('/login')"
          >
            Login
          </button>
        </template>
      </div>
    </div>
    <template v-if="$store.state.isAuthenticated">
      <div class="navbar bg-indigo-1000">
  <div class="d-flex align-items-center">
    <h6 class="ml-auto mx-3 mb-1 mt-1 text-white font-weight-bold" v-text="'Current User: ' + currentUser"></h6>
    <h6 class="ml-auto mx-3 mb-1 mt-1 text-white font-weight-bold" v-text="'Role: ' + currentUserRole"></h6>
  </div>
</div>
</template>

    <router-view>
    </router-view>
  </div>
</div>
<!-- Modal -->
<div v-bind:key="font" v-bind:style="{ fontFamily: font}">
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="exampleModalLabel">Key Dates 📅</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <div
    v-if='selectedDay'
    class='selected-day alert alert-info container-sm'>
    <h4>Date: {{ selectedDay.date.toDateString() }}</h4>
    <ul v-if="selectedDay.attributes.length > 0">
      <li
        v-for='attr in selectedDay.attributes'
        :key='attr.key'>
        {{ attr.customData.title }}
        <button class="btn" @click="speakText(attr.customData.title)"><h5>🔊</h5></button>
      </li>      
    </ul>
    <ul v-else>
      <li>This may be an important day, but no information has been added</li>      
    </ul>
  </div>
  <div
  v-if="!selectedDay"
    class='selected-day alert alert-info container-sm'>
    <h4>Choose a day that has a bar next to it</h4>
    <hr>
    <ul>
      <div class="d-inline-flex">
    <li v-bind:textContent="guidanceText"></li>
    <button class="btn" @click="speakText('')"><h5>🔊</h5></button>
  </div>
    </ul>
  </div>
  <v-calendar is-expanded is-dark :attributes='attributes' @dayclick='dayClicked'></v-calendar>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
</div>

<div class="offcanvas offcanvas-start text-bg-dark" tabindex="-1" id="offcanvasExample" aria-labelledby="offcanvasExampleLabel">
  <div v-bind:key="font" v-bind:style="{ fontFamily: font}">
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="offcanvasExampleLabel">Accessibility Features</h5>
    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    <div>
      <div class="my-2">
  <button class="btn btn-success text-white mx-2" v-on:click="changeSaturation">Toggle Dimmer</button>
</div>
<div class="my-2">
  <button class="btn btn-success text-white mx-2" @click="changeFont">Toggle Font Style</button>
</div>

<hr>
    </div>
  </div>  
  </div>
</div>

</template>  
  
<script>
  import eventsJSON from './json/events.json';
  import axios from 'axios';
  import moment from 'moment'

  export default {
    name: 'App',
    data() {
    return {
      currentUser:'',
      currentUserRole:'',
      currentUserLastLogin:'',
      saturation: 100,
      font: '',
      defaultFont: '',
      guidanceText:'A coloured bar in the below calendar indicates that a day is significant in celebrating learner inclusiveness, wellbeing, accessibility, disability, or another factor of equal value',
      selectedDay: null,
      eventsJSON 
}
    },
    created(){
      if (localStorage.getItem('saturation')) {
      this.saturation = localStorage.getItem('saturation');
    }
    axios.get('/api/v1/LP/getCurrentUser/').then(response => {
    this.currentUser = response.data.username; 
    this.currentUserRole = response.data.role; 
    });

    },
    computed: {
    attributes() {
  return this.eventsJSON.map(t => {
    const dates = [];
    let currentDate = new Date (t.start);
    while (currentDate <= new Date (t.end)) {
      dates.push(currentDate);
      currentDate = new Date(currentDate.getTime() + 24 * 60 * 60 * 1000);
    }

    return {
      key: `todo.${t.id}`,
      dot: false,
      bar:true,
      dates,
      customData: t,
    };
  });
},
    },
  methods: {
    timeElapsed(created_at) {
            const currentDate = moment()
            const createdAt = moment(created_at)
            const date = createdAt.format('MMM D, YYYY [at] h:mm A')
            const elapsed = moment.duration(currentDate.diff(createdAt)).humanize()
                    return `${date} (${elapsed} ago)`
        },
    changeSaturation() {
      this.saturation = this.saturation === 100 ? 50 : 100;
      localStorage.setItem('saturation', this.saturation);
    },
    changeFont() {
      if (this.font !=='OpenDyslexic'){
      this.font = 'OpenDyslexic';
      }
      else { this.font = this.defaultFont; }
    },
    dayClicked(day) { this.selectedDay = day; },
    speakText(text) {
      if (text === '') {
        const speech = new SpeechSynthesisUtterance(this.guidanceText);
        window.speechSynthesis.speak(speech);  
      }
      else {
      const speech = new SpeechSynthesisUtterance(text);
      window.speechSynthesis.speak(speech);
    }
    },
  },
    beforeCreate() {
      this.$store.commit('initalizeStore')
      const token = this.$store.state.token
      if (token) { axios.defaults.headers.common['Authorization'] = "Token " + token
      } else { axios.defaults.headers.common['Authorization'] = "" }      
    }, 
    async mounted(){
      document.title = 'Rezwan: Learning Platform'
      const font = localStorage.getItem('font');
        if (font) { this.font = font;
        } else { this.font = this.defaultFont; }
    },
    watch: {
      font: {
        handler(newFontValue) {
          localStorage.setItem('font', newFontValue);
        }
      },
      '$store.state.isAuthenticated': function () {
        axios.get('/api/v1/LP/getCurrentUser/').then(response => {
        this.currentUser = response.data.username
        this.currentUserRole = response.data.role; 
      })
    },
    }
  }

  </script>

<style>
.bg-indigo-800 {
  background-color: #5e00c3;
}

.bg-indigo-1000 {
  background-color: #7f9ace;
}

#main-calendar {
  display: flex;
}

.selected-day {
  margin-left: 10px;
}


@font-face {
  font-family: 'OpenDyslexic';
  src: url('./assets/fonts/OpenDyslexic.ttf') format('truetype');
}

</style>