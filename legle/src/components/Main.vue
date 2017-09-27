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

      var blob = '{"Authors":["Onbekend"],"Classifications":["Bestuursrecht; Belastingrecht"],"LawArea":["Belastingrecht"],"ProcedureType":"Herziening","SearchNumber":"ECLI:NL:GHDHA:2016:4048","Sources":["Rechtspraak.nl"],"Summary":"Het verzoek tot herziening van de uitspraak van het Hof Den Haag van 11 januari 2013, BK-11/00889 en BK-11/00890 wordt afgewezen. De uitspraken waarvan herziening wordt verzocht zijn gedaan na verwijzing door de Hoge Raad van 25 november 2011, nrs. 10/03270 en 10/05250. Overeenkomstig de verwijzingsopdracht heeft het Hof Den Haag niet geoordeeld over de hoogte van de navorderingsaanslagen en de grondslag waarnaar de verhogingen en boetes worden berekend staan vast.De wijze van verkrijging en gebruik van de informatie van de KB-lux door de Belastingdienst is niet van belang voor de vraag of het aan opzet van verzoeker is te wijten dat te weinig belasting is geheven. Daarvoor is immers uitsluitend relevant of belanghebbende willens en wetens heeft bewerkstelligd dan wel bewust de aanmerkelijke kans heeft aanvaard dat van hem (aanvankelijk) minder belasting is geheven dan hij verschuldigd was. Derhalve zouden de door verzoeker aangevoerde feiten en omstandigheden, waren zij aan het Hof eerder bekend geweest, niet tot andere uitspraken van het Hof als verwijzingshof hebben kunnen leiden.","Timestamp":1498256075,"Title":"Het verzoek tot herziening van de uitspraak van het Hof Den Haag van 11 januari 2013, BK-11/00889 en BK-11/00890 wordt afgewezen. De uitspraken waarvan herziening wordt verzocht zijn gedaan na verwijzing door de Hoge Raad van 25 november 2011, nrs. 10/03270 en 10/05250. Overeenkomstig de verwijzingsopdracht heeft het Hof Den Haag niet geoordeeld over de hoogte van de navorderingsaanslagen en de grondslag waarnaar de verhogingen en boetes worden berekend staan vast.De wijze van verkrijging en gebruik van de informatie van de KB-lux door de Belastingdienst is niet van belang voor de vraag of het aan opzet van verzoeker is te wijten dat te weinig belasting is geheven. Daarvoor is immers uitsluitend relevant of belanghebbende willens en wetens heeft bewerkstelligd dan wel bewust de aanmerkelijke kans heeft aanvaard dat van hem (aanvankelijk) minder belasting is geheven dan hij verschuldigd was. Derhalve zouden de door verzoeker aangevoerde feiten en omstandigheden, waren zij aan het Hof eerder bekend geweest, niet tot andere uitspraken van het Hof als verwijzingshof hebben kunnen leiden.","TopLevelNavigation":["Nederland|Rechtspraak"],"Topic":["Bestuursrecht; Belastingrecht"],"id":23097324}';
      var data = JSON.parse(blob);

      var title = chunkSubstr(shortenString(data.Title, 30), 17);
      title = title.join("\n");

      this.graph = {
            nodes: [{id: data.id, label: title}],
            edges: [],
      }

      /*
      fetch(`http://localhost:5000/document?ecli=${query}`)
        .then((response) => response.json())
        .then((data) => {
          this.graph = {
            nodes: [{id: data.id, label: shortenString(data.Title, 30)}],
            edges: [],
          }
        });*/
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
