<template>
    <div v-bind:key="font" v-bind:style="{ fontFamily: font }">
    <div class="navbar navbar-expand navbar-light bg-indigo-800">
      <h4 class="mx-4 mt-2 text-white me-auto">Rezwan: LMS 🙂</h4>
            <div class="navbar-nav ml-auto mx-4 mb-1 mt-1">

              <button class="btn btn-success nav-item nav-link text-white mx-2" @click="changeFont">Toggle Font Style</button>    
              <!-- Button trigger modal -->
          <button type="button" class="btn btn-success nav-item nav-link text-white mx-2" data-bs-toggle="modal" data-bs-target="#exampleModal">
          Launch Key Dates Calendar
          </button>
        <button
          class="nav-item nav-link btn btn-light mx-2 "
          @click="$router.push('/')"
        >
          Home
        </button>
        <button
          class="nav-item nav-link btn btn-light mx-2"
          @click="$router.push('/about')"
        >
          About
        </button>
        <template v-if="$store.state.isAuthenticated">
          <button
            class="nav-item nav-link btn btn-info mx-2"
            @click="$router.push('/overview')"
          >
            Overview
          </button>
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

<!-- Modal -->
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
      <li>This may well be an important day, but no information has been added</li>      
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
    <router-view></router-view>
  </div>
</template>  
  
<script>
  import eventsJSON from './json/events.json';
  import axios from 'axios';

  export default {
    name: 'App',
    data() {
    return {
      font: '',
      defaultFont: '',
      guidanceText:'A coloured bar in the below calendar indicates that a day is significant in celebrating learner inclusiveness, wellbeing, accessibility, disability, or another factor of equal value',
      selectedDay: null,
      eventsJSON 
}
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
    changeFont() {
      if (this.font !=='OpenDyslexic'){
      this.font = 'OpenDyslexic';
      }
      else { 
        this.font = this.defaultFont;
      }
    },
    dayClicked(day) {
      this.selectedDay = day;
    },
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
  
      if (token) {
        axios.defaults.headers.common['Authorization'] = "Token" + token
      } else {
        axios.defaults.headers.common['Authorization'] = ""
      }
    }, mounted(){
      this.font = this.defaultFont;

    }
  }

  </script>

<style>
.bg-indigo-800 {
  background-color: #5e00c3;
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