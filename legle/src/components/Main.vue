<template>
  <div class="main-container">
    <div class="red-top-bar"></div>
    <graph-view class="abs fs" :showRedBackground="showRedBackground" :graph="graph"></graph-view>
    <widget :onQuery="onQuery"></widget>
    <span class="footer-text">Legle - <span style="opacity: 0.6">legal Google blendle</span> </span>
  </div>
</template>

<script>
import Graph from './Graph.vue'
import Widget from './Widget.vue'

export default {
  components: {
    'graph-view': Graph,
    'widget': Widget,
  },
  name: 'main',
  data () {
    return {
      showRedBackground: true,
      graph: {},
    }
  },
  methods: {
    onQuery(query) {
      this.showRedBackground = false;
      console.log(Widget.data());
      fetch(`http://localhost:5000/document?ecli=${query}`)
        .then((response) => response.json())
        .then((data) => {
          let nodes = [];
          let edges = [];
          for (let doc of data.docs) {
            nodes.push({...doc, label: shortenString(doc.Title, 30)});
          }
          for (let edge of data.references) {
            edges.push({...edge});
          }
          this.graph = {
            nodes,
            edges
          };
        });
    }
  }
}

function shortenString(string, maxLength) {
  return string.substring(0, maxLength) + '...'
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

.red-top-bar {
  position: absolute;
  height: 4px;
  background-color: #e61515;
  width: 100%;
}

.main-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.footer-text {
  opacity: 0.65;
  color: #343434;
  position: absolute;
  bottom: 4px;
  right: 24px;
  font-size: 1.18em;
  transition: all cubic-bezier(0.19, 1, 0.22, 1) 500ms;
}

.footer-text:hover {
  transform: scale(1.125);
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #e03232;
}
</style>
