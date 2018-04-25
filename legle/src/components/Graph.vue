<template>
    <div class="graph-view">
        <div class="red-background fs abs" :class="showRedBackground ? '':'hide'"></div>
        <!-- Will hold the network -->
        <div id="container" class="fullscreen">
            <!-- Welcome message -->
            <div id="info" style="display: none">
                <h1>Law Map</h1>
                <p>A tool for visualizing the connections between law documents by Legle</p>
            </div>
        </div>
        <div class="center-greeting animated fadeIn" :class="(showRedBackground ? '':'hide ') + (isTitle ? '':'no-title')">{{isTitle? 'leegle':'geen resultaten'}}</div>
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
    '#598de0',
    '#3a6cbc',
    '#1e4584',
    '#0d5fe2',
    '#11284c',
    '#6b8ec4',
    '#4a6287',
    '#21385b',
    '#7caaef',
    '#4b8ced',
    '#2c5ba3',
];

const SOURCES = ['Rechtspraak.nl', 'Ove', 'Xpe', 'wet', 'Ken', 'Lok', 'Pra', 'Mem', 'FD', 'Eur',
    'Rij', 'Pen', 'Soc', 'Bel', 'Ten', 'ACM', 'VN', 'Mod', 'Ond', 'Arb', 'NTF', 'Kor', 'De ', 'Lex',
    'Tax', 'RVD', 'Int', 'Mon', 'Tuc', 'Han', 'IEL', 'KiF', 'Dir', 'Fis', 'Zor', 'NJB', 'Cen', 'BRA',
    'NJF', 'Raa', 'Com', 'BNB', 'IE-', 'Prg', 'Ope', 'Mil', 'Blo', 'NJ', 'NDF', 'Zak', 'EPO', 'NZa',
    'SC', 'Reg', 'FED', 'RFR', 'JAR', 'WFR', 'EHR'];

const INSTANCE_MAP = {
    '0': '',
    '1': 'Gerechtshof',
    '2': 'Hoge Raad',
};


const options = {
    nodes: {
        color: '#e00',
        font: {
            color: '#eee',
        },
        shape: 'ellipse',
        mass : 3
    },
    edges: {
        length : 500,
        arrows: {
            to:     {enabled: true, scaleFactor:1}
        },
    },
    layout: {
        randomSeed : 420
    },
    physics: {
        enabled: true,
        barnesHut: {
          gravitationalConstant: -2000,
          centralGravity: 0.3,
          springLength: 150,
          springConstant: 1,
          damping: 0.09,
          avoidOverlap: 0
        },
        stabilization: {
          enabled: true,
          iterations: 180,
          updateInterval: 10,
          onlyDynamicEdges: false,
          fit: true
        },

        maxVelocity: 5
    }
};

export default {
    name: 'main',
    props: [
        'showRedBackground',
        'graph',
        'setWidgetInfo', //Node info that is currently shown in the widget to the left,
        'isTitle',
        'query',
        'querySN',
        'searchOpts',
    ],
    watch: {
        graph: function(g) {
            let { nodes, edges } = g;
            if (this.searchOpts.mode == 'clicks') {
                console.log('filtering edges');
                edges = filterEdges(edges);
                options['edges']['arrows']['to']['enabled'] = false;
            } else {
                options['edges']['arrows']['to']['enabled'] = true;
            }

            if (!this.network) {
                const options = {
                    nodes: {
                        color: '#e00',
                        font: {
                            color: '#eee',
                        },
                        shape: 'ellipse',
                        mass : 3,
                        scaling : {
                          min : 5,
                          max : 50,
                          label: {
                            enabled: true,
                            min: 14,
                            max: 30,
                            maxVisible: 30,
                            drawThreshold: 5
                          },
                        },/*
                        chosen: { //Does not work.
                            node :function(values, id, selected, hovering) {
                                console.log("Chosen change")
                                values.physics = false;
                                values.node.size = 50;
                            }
                        },*/
                    },
                    edges: {
                        length : 1220,
                        arrows: {
                          to:     {enabled: true, scaleFactor:1}
                        },
                        smooth: {
                          type: "diagonalCross",
                          roundness: 0
                        }
                    },
                    layout: {
                        randomSeed : 420
                    },
                    physics: {
                      enabled: true,
                      barnesHut: {
                        gravitationalConstant: -2000,
                        centralGravity: 0.3,
                        springLength: 95,
                        springConstant: 0.00,
                        damping: 0.9,
                        avoidOverlap: 1
                      },
                      stabilization: {
                        enabled: true,
                        iterations: 180,
                        updateInterval: 10,
                        onlyDynamicEdges: false,
                        fit: true
                      }
                    },
                    interaction: {
                        hover: true
                    }
                };

                if (nodes.length > 200) {
                    options['layout'] = {
                        improvedLayout: false
                    };
                };
                const nodesDataSet = new vis.DataSet();
                const edgesDataSet = new vis.DataSet();
                const container = document.getElementById('container');
                this.network = new vis.Network(container, { nodes: nodesDataSet, edges: edgesDataSet }, options);
                this.network.on('stabilizationIterationsDone', function() {
                    console.log("TURN OFF BOUNCE");
                    this.setOptions({physics: {enabled: false}});
                });
                this.draggedNodeId = null;

                this.network.on('dragStart', (selection) => {
                    const id = selection.nodes[0];
                    if (id) {
                        this.draggedNodeId = id;
                        this.nodesDataSet.update({id, fixed: false});
                    }
                });
                this.network.on('dragEnd', () => {
                    if (this.draggedNodeId) {
                        this.nodesDataSet.update({id: this.draggedNodeId, fixed: true});
                        this.draggedNodeId = null;
                    }
                });

                this.network.on('selectNode', (selection) => {
                    //console.log(selection.nodes[0].SearchNumber());
                    var id = selection.nodes[0];
                    this.selected = id;

                    let position = this.network.getPositions(id);
                    position = position[Object.keys(position)[0]];
                    this.network.moveTo({
                        position,
                        animation: {
                            duration: 500,
                            easingFunction: "easeOutQuad"
                        }
                    });
                    for (var n of this.nodes) {
                        if (n.id == id) {
                            console.log("SELECTED", n);
                            this.selectedSN = n.SearchNumber;

                            // Doesn't work ffs
                            //n.size = 500;
                            //n.node.physics = false;

                            var pubNumber = n.PublicationNumber ? n.PublicationNumber: 'Geen';
                            var d = new Date(n.Timestamp * 1000);
                            d = d.toString();
                            d = d.split(' ');
                            d.pop();
                            d.pop();
                            d.pop();
                            d = d.join(' ');
                            if(n.Sources){
                              console.log(n);
                              const fields = {
                                      "ID": n.SearchNumber,
                                      "Bron": n.Sources[0],
                                      "Datum": d,
                                      "Categorie": n.LawArea[0],
                                      "Nummer": pubNumber,
                             };
                             if (n.InstanceType != "0") {
                                 fields['Instantie'] = INSTANCE_MAP[n.InstanceType];
                             }
                             if (n.Verdict === 'True') {
                                 fields['Vernietigd'] = '';
                             }
                              this.setWidgetInfo({
                                  summary: n.Summary,
                                  fields,
                                  id: n.id,
                                  liSearchQuery: n.liSearchQuery,
                                  isWetBook: false,
                                  verdict: shortenString(n.VerdictText, 140),
                              });
                            }
                            else {
                              var fullink = n.Link.split('/');
                              var len = fullink.length;
                              var article = fullink.pop() || fullink.pop();
                              if(len == 4){
                                  article = fullink.pop();
                              }
                              article = capitalizeFirstLetter(article);
                              var firstDigit = article.match(/\d/);
                              var indexed = article.indexOf(firstDigit);
                              article = splitValue(article, indexed);
                              this.setWidgetInfo({
                                  summary: n.Text,
                                  fields: {
                                      "Wetboek" : n.SearchNumber,
                                      "Artikel" : article
                                  },
                                  link : n.Link,
                                  isWetBook: true
                              });
                            }
                            break;
                        }
                    }
                });
                this.network.on('deselectNode', () => {
                    console.log("DESELECT");
                    this.setWidgetInfo(null);
                });
            }

            console.log('stylizing');
            this.stylizeGraph(nodes, edges);
            this.nodes = nodes;

            console.log("Graph changed, n nodes", nodes.length, 'n edjes', edges.length);

            this.nodesDataSet = new vis.DataSet(nodes);
            this.edgesDataSet = new vis.DataSet(edges);

            // create a network
            var data = {
                nodes: this.nodesDataSet,
                edges: this.edgesDataSet
            };

            this.network.setData(data);
            this.network.setOptions(options);
        }
    },

    methods: {
        expandNode: function() {
            this.querySN(this.selectedSN).then((response) => {
                console.log("expandNode");
                console.log(this.selected);
                console.log(response);
                if (this.searchOpts.mode == 'clicks') {
                    console.log('filtering edges');
                    response.references = filterEdges(response.references);
                    options['edges']['arrows']['to']['enabled'] = false;
                } else {
                    options['edges']['arrows']['to']['enabled'] = true;
                }
                console.log("Setting options:");
                console.log(options);
                this.network.setOptions(options);
                this.network.stabilize(1000);
                this.network.on('stabilizationIterationsDone', function() {
                  console.log("TURN OFF BOUNCE");
                  this.setOptions({physics: {enabled: false}});
                  console.log(this.options)
                });

                this.stylizeGraph(response.docs, response.references);
                for (let doc of response.docs) {
                    try {
                        this.nodesDataSet.add(doc);
                        this.nodes.push(doc);
                    } catch (e) { }
                }

                for (let ref of response.references) {
                    let eds = this.edgesDataSet;
                    let found = false;
                    for(let key of Object.keys(eds._data)) {
                        let edge = eds._data[key];
                        if (edge.from === ref.from && edge.to === ref.to) {
                            found = true;
                            break;
                        }
                    }
                    if (!found) {
                        eds.add(ref);
                    }
                }

            });
        },

        stylizeGraph: function(nodes, edges) {
            for (var i = 0; i < nodes.length; i++) {
                var color = '#d6e6ff';
                var fontColor = '#EEE';

                nodes[i]['node'] = {title: nodes[i].Title}  //Doesn't actually work
                nodes[i]['title'] = nodes[i].Title; //Doesn't actually work
                /*
                nodes[i]['chosen'] = { //Should work, but doens't
                    'node': function(values, id, selected, hovering) {
                                console.log("Chosen change")
                                values.physics = false;
                                values.node.size = 50;
                            }
                }*/

                if(nodes[i].Sources) {
                  var src = nodes[i].Sources[0];
                  for (var j = 0; j < SOURCES.length; j++) {
                      var colorIndex = j % COLORS.length;

                      if (src.startsWith('Rechtspraak.nl')) {
                          color = '#EEE';
                          fontColor = '#555';
                      }
                      else if (src.startsWith(SOURCES[j])) {
                          color = COLORS[colorIndex];
                          break;
                      }
                  }
                }

                if (color == '#EEE' || color == '#68ADFF' || color == '#d6e6ff') {
                    fontColor = '#555';
                }

                nodes[i]['color'] = color;
                nodes[i]['font'] = {
                    color: fontColor,
                };

                let label = '';
                if (!nodes[i].SearchNumber) {
                    if(nodes[i].Sources){
                        nodes[i].SearchNumber = nodes[i].Sources[0];
                    }
                    else {
                      nodes[i].SearchNumber = nodes[i].Law;
                    }
                    if(nodes[i].Summary){
                        nodes[i].liSearchQuery = nodes[i].Summary.substr(0, 120);
                    }
                    else {
                      nodes[i].liSearchQuery = 'law2';
                    }
                    if(!nodes[i].Law){
                        label = chunkSubstr(shortenString(nodes[i].SearchNumber, 57), 20).join('\n');
                    }
                    else{
                      label = chunkSubstr(nodes[i].SearchNumber, 20).join('\n');
                    }
                } else {
                    nodes[i].liSearchQuery = nodes[i].PublicationNumber;
                    label = '\n' + nodes[i].SearchNumber + '\n';
                }
                nodes[i]['label'] = label;
                if(nodes[i].Law){
                  nodes[i]['shape'] = 'box';
                }
                nodes[i]['value'] = 100000*nodes[i]['PageRank'];
                if(nodes[i].Law) {
                    nodes[i]['value'] = 3.0;
                }
                if (isNaN(nodes[i]['value'])) {
                    nodes[i]['value'] = 1.5;
                }
                console.log(nodes[i]);
                console.log(label);
            }
            for(var i = 0; i < edges.length; i++){
                let count = edges[i].count;
                edges[i]['value'] = count;
            }

        },


    },

    mounted: function() {
        document.body.onkeyup = (e) => {
            if (e.keyCode === 32) {
                this.expandNode();
            }
        }
    },

    data() {
        return {
            selected: null,
            selectedSN: null
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

function filterEdges(edges) {
    const result = [];
    const added = {};
    for (let edge of edges) {
        let s = edge.from.toString() + edge.to.toString();
        let r = edge.to.toString() + edge.from.toString();
        if (added[s] || added [r]) {
            continue;
        }
        added[s] = true;
        result.push(edge);
    }
    return result;
}

function splitValue(value, index) {
    return value.substring(0, index) + " " + value.substring(index);
}

function shortenString(string, maxLength) {
  if (!string) {
      return;
  }
  return string.substring(0, maxLength) + '...';
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}
</script>

<style scoped>
.graph-view {
    width: 100%;
    height: 100%;
    background-color: #eff1f5;
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

.red-background.hide {
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

.center-greeting.hide {
    opacity: 0;
    visibility: hidden;
}
</style>
