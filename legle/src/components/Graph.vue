<template>
  <div class="graph-view">
    <div class="red-background fs abs" :class="showRedBackground ? '':'hide'"></div>
      <!-- Will hold the network -->
      <div id="container" class="fullscreen">
        <!-- Welcome message -->
        <div id="info">
          <h1>Law Map</h1>
          <p>A tool for visualizing the connections between law documents by Legle</p>
        </div>
      </div>
    <div class="center-greeting animated fadeIn" :class="showRedBackground ? '':'hide'">legle</div>
  </div>
</template>

<script>
import 'vis';

export default {
  name: 'main',
  props: ['showRedBackground', 'graph'],
  watch: {
    graph: function(g) {
      let {nodes, edges} = g;

      //nodes[0]['color'] = '#00F';

      let nodesDataSet = new vis.DataSet(nodes);
      let edgesDataSet = new vis.DataSet(edges);

      // create a network
      var container = document.getElementById('container');
      var data = {
        nodes: nodesDataSet,
        edges: edgesDataSet
      };
      var options = {
          nodes: {
              color: '#e00',
              font: {
                  color: '#eee',
              },
              shape: 'ellipse',
          }
      };
      var network = new vis.Network(container, data, options);
      network.on('select', (a)=>{console.log("SELECT", this.graph.nodes)});
    }
  },

  mounted: function () {},

  data () {
    return {
    }
  }
}
</script>

<style scoped>
.graph-view {
    width: 100%;
    height: 100%;
    background-color: #f2f2f2;
    position: absolute;
    z-index: 0;
}

.red-background {
    background: linear-gradient(290deg, #1c08c6, #59d3f7);
    transition: all ease-in-out 500ms;
    position: absolute;
    z-index: 1;
    pointer-events: none;
}

.red-background.hide{
    opacity: 0;
}

.center-greeting {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    color: #fff;
    font-size: 12.5em;
    z-index: 2;
    text-shadow: 1px 2px 3px rgba(0, 0, 0, 0.3);
    transition: all ease-in-out 200ms;
    opacity: 1;
}

.center-greeting.hide{
    opacity: 0;
    visibility: hidden;
}
</style>
