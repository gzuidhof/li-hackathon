<template>
<form class="sidebar" v-on:submit.prevent="onEnter">
    <div class="widget widget-search animated fadeInLeft">
      <input class="search-input" placeholder="Voer referentienummer in.." v-model="searchQuery"></input>
    </div>

  <div v-if="widgetVisible" class="animated fadeIn">
    <div class="widget widget-main">
        <div class="widget-section">
            <h3>Document</h3>
        </div>
        <div class="widget-content">
        <table>
            <tbody>
                <tr v-for="(value, key) in widgetInfo.fields">
                <td class="action">
                    <a>✔</a>
                </td>
                <td class="key">{{key}}
                </td>
                <td class="content">{{value}}
                </td>
                </tr>
            </tbody>
        </table>
        </div>


        <div class="widget-content">
            <h4 style="margin-top: -12px; margin-bottom: 6px;">Samenvatting</h4>
            <p class="summary">{{widgetInfo.summary}}</p>
        </div>
        
        <div v-if="widgetInfo.verdict" class="widget-content">
            <h4 style="margin-top: -12px; margin-bottom: 6px;">Conclusie</h4>
            <p class="summary">{{widgetInfo.verdict}}</p>
        </div>

        <div class="li-button-wrapper" :href="widgetInfo.id">
            <a target='_blank' :href="leftLink">
            <div class="li-button mr">
            Openen
            </div>
            </a>
            <a target='_blank' :href="rightLink">
            <div class="li-button">
            {{rightText}}
            </div>
            </a>
        </div>

    </div>

  </div>
  </form>
</template>

<script>
import Graph from './Graph.vue'
export default {
  props: ['onQuery', 'widgetInfo', 'widgetVisible'],
  methods: {
      onEnter(asdf){
          console.log("Please search nao ", this.searchQuery);
          this.onQuery(this.searchQuery);
          this.$route.query.q = this.searchQuery;
      }
  },
  data () {
    return {
        searchQuery: "",
    }
  },
  computed: {
    leftLink() {
        if(!this.widgetInfo) return;
        if (this.widgetInfo.isWetBook) {
            return 'http://www.maxius.nl' + this.widgetInfo.link;
        }
        else {
            return 'http://www.legalintelligence.com/documents/' + this.widgetInfo.id;
        }
    },
    rightLink() {
        if(!this.widgetInfo) return;
        if (this.widgetInfo.isWetBook) {
            var query = this.widgetInfo.link;
            query = query.replace(/-/g, ' ');
            query = query.replace(/\//g, ' ');
            return 'https://www.legalintelligence.com/SearchResults?q=' + query;
        }
        else {
            return 'https://www.legalintelligence.com/SearchResults?q=' + this.widgetInfo.liSearchQuery;
        }
    },
    rightText() {
        return 'Zoeken in Legal Intelligence';
    }
  },
  created() {
    if (this.$route.query.q) {
      this.searchQuery = this.$route.query.q.trim();
      if (this.searchQuery.endsWith('.') || this.searchQuery.endsWith(',')) {
          this.searchQuery = this.searchQuery.substring(0, this.searchQuery.length - 1).trim();
      }
      this.onEnter();
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

.sidebar {
    display: flex;
    flex-direction: column;
    margin: 28px;
    width: 360px;
    position: absolute;
    z-index: 1;
}

.key {
    font-weight: bold;
}

.widget {
    display: flex;
    flex-direction: column;
    padding: 8px;
    background-color: #fdfdfd;
    width: 360px;
    border-radius: 7px;
    box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.22);
    color: #777;
}

.widget-main {
    min-height: 480px;
}

.widget-search {
    margin-bottom: 24px;
    animation-duration: 1s;
}

.search-input {
    font-size: 1.45em;
    border-style: none;
    padding: 5px 8px;
}

.widget-section {
    border-bottom: 2px solid #ddd;
}

.widget-section h3 {
    font-weight: normal;
}

.widget-content {
    padding: 12px 4px;
}

.summary {
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    color: #666;
}

td {
    padding: 0px 2px;
}

.li-button-wrapper{
    /*margin: 0 auto;*/
    position: absolute;
    bottom: 18px;
    right: 18px;
    text-decoration: none !important;
    display: flex;
}

.li-button-wrapper a {
    text-decoration: none !important;
}

.li-button {
    cursor: pointer;
    background-color: #f7f7f7;
    font-size: 1.05em;
    text-align: center;
    color: #828080;
    padding: 2px 10px;
    border-radius: 4px;
    border: 1px solid #ccc;
}

.li-button:hover {
    text-decoration: none;
    background-color: #eee;
}

.mr {
    margin-right: 12px;
    background-color: #3f60da;
    color: #eee;
    border: 1px solid #eee;
}

.mr:hover {
    background-color: #4f70ea;
}

</style>
