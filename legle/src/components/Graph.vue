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

const COLORS = [
    '#EEE', //light
    '#68ADFF', //light
    '#2D547E',
    '#7295A6',
    '#3F60D3',
    '#A06EC9',
    '#813BCE'
]

const SOURCES = ['Rechtspraak.nl', 'Ove', 'Xpe', 'wet', 'Ken', 'Lok', 'Pra', 'Mem', 'FD', 'Eur',
'Rij', 'Pen', 'Soc', 'Bel', 'Ten', 'ACM', 'VN', 'Mod', 'Ond', 'Arb', 'NTF', 'Kor', 'De ', 'Lex',
'Tax', 'RVD', 'Int', 'Mon', 'Tuc', 'Han', 'IEL', 'KiF', 'Dir', 'Fis', 'Zor', 'NJB', 'Cen', 'BRA',
'NJF', 'Raa', 'Com', 'BNB', 'IE-', 'Prg', 'Ope', 'Mil', 'Blo', 'NJ', 'NDF', 'Zak', 'EPO', 'NZa',
'SC', 'Reg', 'FED', 'RFR', 'JAR', 'WFR', 'EHR']

export default {
  name: 'main',
  props: [
      'showRedBackground',
      'graph',
      'setWidgetInfo' //Node info that is currently shown in the widget to the left
    ],
  watch: {
    graph: function(g) {
      let {nodes, edges} = g;

      console.log("Graph changed, n nodes", nodes.length);

      for(var i = 0; i < nodes.length; i++) {
          
          var src = nodes[i].Sources[0];
          var color = '#813BCE';
          var fontColor = '#EEE';

          for(var j = 0; j < SOURCES.length; j++) {
              var colorIndex = j % COLORS.length;
              if (src.startsWith(SOURCES[j])) {
                  color = COLORS[colorIndex];
                  break;
              }
          }

          if (color == '#EEE' || color == '#68ADFF') {
              fontColor = '#555';
          }

          nodes[i]['color'] = color;
          nodes[i]['font'] = {
              color: fontColor,
          }

      }

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
      network.on('selectNode', (selection) => {
          var id = selection.nodes[0];
          for (var n of this.graph.nodes) {
              if (n.id == id) {
                  console.log("SELECTED", n);
                  this.setWidgetInfo({
                      summary: n.Summary,
                      fields: {
                          "ID": n.SearchNumber,
                          "Bron": n.Sources[0],
                          "Datum": n.Timestamp,
                          "Categorie": n.LawArea[0],
                      },
                      id: n.id,
                  });
                  break;
              }
          }
        });
     network.on('deselectNode', () => {
         console.log("DESELECT");
         this.setWidgetInfo(null);
     })
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
