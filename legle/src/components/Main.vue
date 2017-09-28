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
      showRedBackground: false,
      graph: {},
    }
  },
  methods: {
    onQuery(query) {
      this.showRedBackground = false;

      if (query === '') {
        this.showRedBackground = true;
        return;
      }
      console.log(Widget.data());

      fetch(`http://1366ee3f.ngrok.io/document?ecli=${query}`)
        .then((response) => response.json())
        .then((data) => {
          let nodes = [];
          let edges = [];
          let alreadyAdded = [];
          for (let doc of data) {
            let id = doc.document.id;
            if (alreadyAdded.indexOf(id) === -1) {
              const titleChunks = chunkSubstr(shortenString(doc.document.Title, 50), 14);
              var title = titleChunks.join("\n");
              title = doc.document.SearchNumber;
              nodes.push({...doc.document, label: title});
              alreadyAdded.push(id);
            }
            for (let link of doc.links) {
              let id = link.id;
              if (alreadyAdded.indexOf(id) === -1) {
                const titleChunks = chunkSubstr(shortenString(link.Title, 50), 14);
                var title = titleChunks.join("\n");
                title = link.SearchNumber;
                nodes.push({...link, label: title});
                alreadyAdded.push(id);
              }
              edges.push({from: doc.document.id, to: link.id});
            }
          }
        this.graph = {
          nodes,
          edges
          };
        });
    }
  }
}

function chunkSubstr(str, size) {
  var numChunks = Math.ceil(str.length / size),
      chunks = new Array(numChunks);

  for(var i = 0, o = 0; i < numChunks; ++i, o += size) {
    chunks[i] = str.substr(o, size);
  }

  return chunks;
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
