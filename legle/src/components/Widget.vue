<template>
<form class="sidebar" v-on:submit.prevent="onEnter">
    <div class="widget widget-search animated fadeInLeft">
      <input class="search-input" placeholder="Enter an ECLI number.." v-model="searchQuery"></input>
    </div>

  <div v-if="widgetVisible">
    <div class="widget widget-main">
        <div class="widget-section">
            <h3>Document</h3>
        </div>
        <div class="widget-content">
        <table>
            <tbody>
                <tr v-for="(value, key) in fields">
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
            <p class="summary">{{summary}}</p>
        </div>



    </div>

  </div>
  </form>
</template>

<script>
import Graph from './Graph.vue'
export default {
  props: ['onQuery'],
  methods: {
      onEnter(asdf){
          console.log("Please search nao ", this.searchQuery);
          this.onQuery(this.searchQuery);
      }
  },
  data () {
    return {
        widgetVisible: true,
        searchQuery: "",
        fields: {
            "ECLI": "ECLI:asdf234123asdff",
            "Datum": "20-07-2013",
            "Bron": "www.rechtspraak.nl",
        },
        summary: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris maximus purus id lacus elementum placerat. Ut id efficitur urna. Nunc sed porta leo, vitae imperdiet metus. Sed commodo ipsum arcu, non dignissim lectus blandit et. Vestibulum at ex leo. Sed imperdiet urna ut justo semper tempor. Fusce ultrices convallis dignissim. Cras accumsan viverra est quis rutrum. Suspendisse potenti. Ut sodales eu justo eget malesuada. Integer tincidunt felis quis ex scelerisque varius.",
    }
  }
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
    min-height: 420px;
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

</style>
