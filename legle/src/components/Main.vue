<template>
  <div class="main-container">
    <div class="red-top-bar" :style="{opacity: showRedBackground ? '0': '1.0'}"></div>
    <graph-view class="abs fs" :searchOpts="searchOpts" :showRedBackground="showRedBackground" :graph="graph" :setWidgetInfo="setWidgetInfo" :isTitle="isTitle" :query="query" :querySN="querySN"></graph-view>
    <widget :onQuery="onQuery" :widgetVisible="widgetVisible" :widgetInfo="widgetInfo"></widget>
    <options :isOnBackground="showRedBackground" :onOptsChange="onOptsChange"></options>
    <span class="footer-text" :style="{color: showRedBackground ? '#f3f3f3' : '#343434'}">leegle ✦ <span style="opacity: 0.8; font-style: italic">niet zoeken maar ontdekken</span> </span>
  </div>
</template>

<script>
import Graph from './Graph.vue'
import Widget from './Widget.vue'
import Options from './Options.vue'

const SERVER_URL = 'http://localhost:5000';

export default {
  components: {
    'graph-view': Graph,
    'widget': Widget,
    'options': Options,
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
        liSearchQuery: "",
      },
      widgetVisible: false,
      isTitle: true,
      isWetBook: false,
      searchOpts: {
        mode: 'referenties', //or 'clicks'
        depth: 1,
      },
      lastQuery: "",
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
    query(id) {
      return fetch(`${SERVER_URL}/solrdocument?id=${id}&depth=${this.searchOpts.depth}&mode=${this.searchOpts.mode}`)
        .then((response) => response.json());
    },
    querySN(sn) {
      return fetch(`${SERVER_URL}/solrdocument?ecli=${sn}&depth=${this.searchOpts.depth}&mode=${this.searchOpts.mode}`)
        .then((response) => response.json());
    },
    onOptsChange(opts) {
      var changedMode = opts.mode != this.searchOpts.mode;
      this.searchOpts = opts;

      if (changedMode) {
        this.onQuery(this.lastQuery);
      }
    },
    onQuery(query) {
      console.log('onQuery');
      this.lastQuery = query;
      if (query === '') {
        this.showRedBackground = true;
        this.widgetVisible = false;
        this.isTitle = true;
        return;
      }
      console.log(Widget.data(), query, this.searchOpts);

      fetch(`${SERVER_URL}/solrdocument?ecli=${query}&depth=${this.searchOpts.depth}&mode=${this.searchOpts.mode}`)
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          this.graph = {
            nodes: data.docs,
            edges: data.references,
          };
          this.showRedBackground = false;
          if (this.graph.nodes.length == 0) {
            this.showRedBackground = true;
            this.isTitle = false;
          }
        });
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

.red-top-bar {
  position: absolute;
  height: 2px;
  background-color: #236fb1;
  width: 100%;
  z-index: 5;
  transition: all 450ms ease-in-out;
}

.main-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.footer-text {
  opacity: 0.7;
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
  opacity: 0.8;
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

a, a:hover {
  color: #404cff;
  text-decoration: none;
}
</style>
