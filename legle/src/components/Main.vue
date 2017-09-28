<template>
  <div class="main-container">
    <div class="red-top-bar"></div>
    <graph-view class="abs fs" :showRedBackground="showRedBackground" :graph="graph" :setWidgetInfo="setWidgetInfo" :isTitle="isTitle"></graph-view>
    <widget :onQuery="onQuery" :widgetVisible="widgetVisible" :widgetInfo="widgetInfo"></widget>
    <span class="footer-text" :style="{color: showRedBackground ? '#f3f3f3' : '#343434'}">Legle ✦ <span style="opacity: 0.8; font-style: italic">niet zoeken maar ontdekken</span> </span>
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
      widgetInfo: {
        fields: [],
        summary: "",
        id: "",
      },
      widgetVisible: false,
      isTitle: true,
    }
  },
  methods: {
    setWidgetInfo(info) {
      if(info) {
        this.widgetInfo = info;
        this.widgetVisible = true;
      }
      else {
        this.widgetInfo = {fields:[], summary: "", id: ""}
        this.widgetVisible = false;
      }
    },
    onQuery(query) {

      if (query === '') {
        this.showRedBackground = true;
        this.widgetVisible = false;
        this.isTitle = true;
        return;
      }
      console.log(Widget.data(), query);

      fetch(`http://bf64f785.ngrok.io/document?ecli=${query}`)
        .then((response) => response.json())
        .then((data) => {
          let nodes = [];
          let edges = [];
          for (let doc of data.docs) {
            let label = '';
            if (!doc.SearchNumber) {
              doc.SearchNumber = doc.Title;
              label = chunkSubstr(shortenString(doc.SearchNumber, 57), 20).join('\n');
            } else {
              label = '\n' + doc.SearchNumber + '\n';
            }
            nodes.push({...doc, label})
          }
          for (let edge of data.references) {
            edges.push({...edge});
          }
          this.graph = {
            nodes,
            edges
          };
          this.showRedBackground = false;
          if (nodes.length == 0) {
            this.showRedBackground = true;
            this.isTitle=false;
          }
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
  bottom: 6px;
  right: 42px;
  font-size: 1.78em;
  transition: all cubic-bezier(0.19, 1, 0.22, 1) 400ms;
}

.footer-text span {
  font-size: 0.75em;
}

.footer-text:hover {
  transform: translateX(-40px);
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
