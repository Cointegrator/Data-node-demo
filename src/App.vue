<template>
  <div id="app">
    <panel-board msg="Welcome to the system!"/>
  </div>
</template>

<script>
import PanelBoard from './components/PanelBoard.vue'

export default {
  name: 'App',
  components: {
    PanelBoard,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
