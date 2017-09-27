<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style>
html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100%;
  width: 100%;
  position: relative;
}

html, body, h1, h2, h3, h4 {
    margin: 0;
    padding: 0;
    vertical-align: baseline;
    background: transparent;
}

*:focus {
    outline: none;
}

.abs {
  position: absolute;
}

.fs {
  width: 100%;
  height: 100%;
}

* {
  background-color: transparent;
}

p {
  margin-top: 2px;
  margin-bottom: 2px;
}
</style>
