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
    <div class="center-greeting animated fadeIn"
    :class="(showRedBackground ? '':'hide ') + (isTitle ? '':'no-title')">{{isTitle? 'legle':'geen resultaten'}}</div>
  </div>
</template>

<script>
import 'vis';

const COLORS = [
    '#107FC9', //light
    '#0E4EAD',
    '#0B108C',
    '#0C0F66',
    '#07093D',
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
      'setWidgetInfo', //Node info that is currently shown in the widget to the left,
      'isTitle',
    ],
  watch: {
    graph: function(g) {
      let {nodes, edges} = g;

        if (!this.network) {
            const options = {
            nodes: {
                color: '#e00',
                font: {
                    color: '#eee',
                },
                shape: 'ellipse',
            }
        };

        if(nodes.length > 200) {
            options['layout'] = {
                improvedLayout: false
            };
        };
        const nodesDataSet = new vis.DataSet();
        const edgesDataSet = new vis.DataSet();
        const container = document.getElementById('container');
        this.network = new vis.Network(container, {nodes: nodesDataSet, edges: edgesDataSet}, options);
      }

      console.log("Graph changed, n nodes", nodes.length, 'n edjes', edges.length);

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
          };

      }

      let nodesDataSet = new vis.DataSet(nodes);
      let edgesDataSet = new vis.DataSet(edges);

      // create a network
      var data = {
        nodes: nodesDataSet,
        edges: edgesDataSet
      };

      this.network.setData(data);

      this.network.on('selectNode', (selection) => {
          var id = selection.nodes[0];
          let position = this.network.getPositions(id);
          position = position[Object.keys(position)[0]];
          this.network.moveTo({
              position,
              animation: {
                  duration: 500,
                  easingFunction: "easeOutQuad"
              }
          });
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
        this.network.on('deselectNode', () => {
            console.log("DESELECT");
            this.setWidgetInfo(null);
        });
    }
  },

  mounted: function () {

  },

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
    background: linear-gradient(290deg, #1e0fa9, #59d3f7);
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
    transition: opacity ease-in-out 200ms;
    opacity: 1;
}

.no-title {
    font-size: 3em;
}

.center-greeting.hide{
    opacity: 0;
    visibility: hidden;
}
</style>
