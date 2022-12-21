<template>
    <nav class="container-fluid navbar navbar-expand-lg navbar-light bg-indigo-800">
      <h4 class="mx-4 text-white container-fluid">Rezwan: LMS</h4>
      <div class="navbar-nav ml-auto mx-4 mb-1 mt-1">
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
            class="nav-item nav-link text-white btn btn-secondary mx-2"
            @click="$router.push('/login')"
          >
            Login
          </button>
        </template>
      </div>
    </nav>

    <div
    v-if='selectedDay'
    class='selected-day alert alert-info container-sm'>
    <h4>{{ selectedDay.date.toDateString() }}</h4>
    <ul>
      <li
        v-for='attr in selectedDay.attributes'
        :key='attr.key'>
        {{ attr.customData.title }}
      </li>      
    </ul>
  </div>
  <div
  v-else
    class='selected-day alert alert-info container-sm'>
    <h4>Choose a day that has a bar near it</h4>
    <hr>
    <ul>
      <li>
        A coloured bar indicates that a day is significant in celebrating learner inclusiveness, wellbeing, accessibility, disability, or another factor of equal value
      </li>
    </ul>
  </div>

  <v-calendar is-dark :attributes='attributes' @dayclick='dayClicked'></v-calendar>

    <router-view></router-view>
  </template>  
  
<script>
  import eventsJSON from './json/events.json';
  import axios from 'axios';

  export default {
    name: 'App',
    data() {
    return {
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
    dayClicked(day) {
      this.selectedDay = day;
    }
  },
    beforeCreate() {
      this.$store.commit('initalizeStore')
      const token = this.$store.state.token
  
      if (token) {
        axios.defaults.headers.common['Authorization'] = "Token" + token
      } else {
        axios.defaults.headers.common['Authorization'] = ""
      }
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
</style>