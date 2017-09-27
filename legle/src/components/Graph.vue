<template>
  <div class="graph-view">
    <div>
      <div id="formbox" class="transparent-blur">
        <button id="random" type=button title="Random article">
          <i class="icon ion-shuffle"></i>
        </button>
        <button id="submit" type="button" title="Enter the name of a wikipedia page, then press 'Go'">
          Go
        </button>
        <div id="input" class="commafield" data-placeholder="Wikipedia"> </div>
      </div>

      <!-- Will hold the network -->
      <div id="container" class="fullscreen">
        <!-- Welcome message -->
        <div id="info">
          <h1>Law Map</h1>
          <p>A tool for visualizing the connections between Law pages by Legle</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import '../js/main.js'
import '../js/api.js'
import '../js/bindings.js'
import '../js/commafield.js'
import '../js/help.js'
import '../js/helpers.js'
import '../js/loadsaved.js'
import '../js/main_functions.js'
import '../js/modals.js'
import '../js/network_serialize.js'
import '../js/progress.js'

function test(){
  return 2;
}

export default {
  name: 'main',
  data () {
    return {}
  },
  mounted () {

  }
}
</script>

<style scoped>
.graph-view {
    width: 100%;
    height: 100%;
    background-color: #f2f2f2;
    position: absolute;
    z-index: -1;
}
</style>
