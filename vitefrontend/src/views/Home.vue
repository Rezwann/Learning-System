<template>
    <div class="container-sm">
          <div class="mb-4 m-5"></div>
    <div><h1 class="text-center">Home</h1></div>
    <div class="alert alert-success" role="alert">
  <h4 class="alert-heading">Hello!</h4>
  <p ref="text">Hey, what's good </p>
  <button class="btn btn-info" @click="speakText">🔊</button>
  <hr>
  <p class="mb-0">Whenever you need to, be sure to use margin utilities to keep things nice and tidy.</p>
</div>
</div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      text: ''
    };
  },
  mounted() {
    this.text = this.$refs.text.textContent;
  },
  methods: {
    speakText() {
      const speech = new SpeechSynthesisUtterance(this.text);
      window.speechSynthesis.speak(speech);
    }
  }
};
</script>