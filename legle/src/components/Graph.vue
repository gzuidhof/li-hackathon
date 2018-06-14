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

const HIERARCHY = {
  'Onbekend': 6,
  'Rechtbanken': 5,
  'Gerechtshoven': 4,
  'Centrale Nederlandse rechtscolleges': 3,  // = Hoge Raad
  'Rijksoverheid': 2,
  'Europese gerechtshoven': 1,
  'Europese instellingen': 0
};

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
        mass : 3,
        scaling : {
          min : 14,
          max : 500,
          label: {
            enabled: true,
            min: 14,
            max: 30,
            maxVisible: 30,
            drawThreshold: 5
          },
        },
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
        enabled: false,
        barnesHut: {
          gravitationalConstant: -2000,
          centralGravity: 0.3,
          springLength: 150,
          springConstant: 1,
          damping: 0.09,
          avoidOverlap: 0
        },
        stabilization: {
          enabled: false,
          iterations: 180,
          updateInterval: 10,
          onlyDynamicEdges: false,
          fit: false
        },

        maxVelocity: 5
    },
    interaction: {
        hover: true
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
                          min : 0,
                          max : 500,
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
                      enabled: false,
                      barnesHut: {
                        gravitationalConstant: -2000,
                        centralGravity: 0.3,
                        springLength: 95,
                        springConstant: 0.00,
                        damping: 0.9,
                        avoidOverlap: 1
                      },
                      stabilization: {
                        enabled: false,
                        iterations: 180,
                        updateInterval: 10,
                        onlyDynamicEdges: false,
                        fit: false
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
                }
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
                    if (id && this.clusters.indexOf(id) < 0) {
                        this.draggedNodeId = id;
                        this.nodesDataSet.update({id, fixed: false});
                    }
                });
                this.network.on('dragEnd', () => {
                    if (this.draggedNodeId && !this.draggedNodeId.startsWith("cluster")) {
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
                    console.log("selectNode selection", selection);
                    console.log("clusters: ", this.clusters);
                    console.log("cluster index?: ", this.clusters.indexOf(selection.nodes[0]));
                    // Check if the selected node is a cluster of nodes
                    let cluster_index = this.clusters.indexOf(this.selected);
                    if (cluster_index >= 0) {
                      this.selectedSN = this.selected
                    } else {
                      // Otherwise, find the selected node
                      for (var n of this.nodes) {
                        if (n.id == id) {
                          console.log("SELECTED", n);
                          this.selectedSN = n.SearchNumber;
                          // Set the widgetinfo
                          var pubNumber = n.PublicationNumber ? n.PublicationNumber: 'Geen';
                          let timestamp = (n.Timestamp).toString();
                          timestamp = timestamp.slice(0, 4) + '-' + timestamp.slice(4, 6) + '-' + timestamp.slice(6,8);
                          var d = new Date(timestamp);
                          d = d.toString();
                          d = d.split(' ');
                          d.pop();
                          d.pop();
                          d.pop();
                          d = d.join(' ');
                          if(n.Sources){
                            const fields = {
                              "ID": n.SearchNumber,
                              "Bron": n.Sources[0],
                              "Datum": d,
                              "Categorie": n.LawArea[0],
                              "Nummer": pubNumber,
                              "Institution Group": n.IssuingInstitution_Group
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
                    }


                });
                this.network.on('deselectNode', () => {
                    console.log("DESELECT");
                    this.setWidgetInfo(null);
                });
            }

            console.log('stylizing');

            this.clusters = [];
            // this list maintains which clusters have been manually opened by the user;
            // we don't want to accidentally re-cluster them when the graph is expanded
            this.expandedClusterKeys = [];
            this.stylizeGraph(nodes, edges);
            console.log("clusters: " + this.clusters);

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
            this.clusterNodes();
        }
    },

    methods: {
        expandNode: function() {
            console.log("Selected:");
            console.log(this.selectedSN);
            let clusterIndex = this.clusters.indexOf(this.selectedSN);
            // Check if we want to expand a cluster
            if (clusterIndex >= 0)
            {
              // Open it
              this.network.openCluster(this.selectedSN);
              // Remove it from the list of cluster indices
              this.clusters.splice(clusterIndex, 1);
              // Add it to the manually expanded clusters list
              this.expandedClusterKeys.push(this.selectedSN);
            } else {
              // Otherwise, send a query for the selected node and display the results
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
                this.network.on('stabilizationIterationsDone', function () {
                  console.log("TURN OFF BOUNCE");
                  this.setOptions({physics: {enabled: false}});
                  console.log(this.options)
                });

                // We expand the clusters for a brief moment, otherwise new edges that point towards documents
                // within a cluster are not formed
                this.expandClusters();
                this.stylizeGraph(response.docs, response.references);

                for (let doc of response.docs) {
                  try {
                    this.nodesDataSet.add(doc);
                    this.nodes.push(doc);
                  } catch (e) {
                  }
                }

                for (let ref of response.references) {
                  let eds = this.edgesDataSet;
                  let found = false;
                  for (let key of Object.keys(eds._data)) {
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


                this.clusterNodes();
              });
            }
        },

        stylizeGraph: function(nodes, edges, updateClusters = true) {
            let bwb_groups = {};

            for (var i = 0; i < nodes.length; i++) {
                var color = '#d6e6ff';
                var fontColor = '#EEE';

                //nodes[i]['node'] = {title: nodes[i].Title};  //Doesn't actually work

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

                if (nodes[i].SearchNumber.startsWith('BWB')) {
                    let bwbPrefix = nodes[i].SearchNumber.split('/')[0];
                    if (bwbPrefix in bwb_groups) {
                        bwb_groups[bwbPrefix].push(i);
                    } else {
                        bwb_groups[bwbPrefix] = [i];
                    }
                }

                nodes[i]['x'] = Math.sqrt(nodes[i]['Timestamp'])*20;
                nodes[i]['y'] = getNodeHierarchy(nodes[i]) * 500;

                nodes[i].fixed = {
                  x: true,
                  y: true
                };

                //nodes[i]['label'] = label;

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
                nodes[i]['value'] = nodes[i]['value'] * 1000;
            }

            // Edge thickness
            for(var i = 0; i < edges.length; i++) {
              let count = edges[i].count;
              edges[i]['value'] = count;
            }

            if (updateClusters) {
              console.log('bwb groups:');
              console.log(bwb_groups);

              for (let key in bwb_groups) {
                if (bwb_groups.hasOwnProperty(key)) {
                  if (bwb_groups[key].length > 1) {
                    for (var i = 0; i < bwb_groups[key].length; i++) {
                      let nodeID = bwb_groups[key][i];
                      nodes[nodeID]['clusterID'] = key;
                    }
                    // Don't add the cluster if it already exists, or it was manually expanded by the user
                    if (this.clusters.indexOf(key) < 0 && this.expandedClusterKeys.indexOf(key) < 0)
                      this.clusters.push(key);
                  }
                }
              }
              console.log("clusters: ");
              console.log(this.clusters);
            }
        },
        clusterNodes: function() {
            var clusterOptionsByData;
            for (var i = 0; i < this.clusters.length; i++) {
              let clusterID = this.clusters[i];
              console.log("Clustering:");
              console.log(clusterID);
              clusterOptionsByData = {
                processProperties: function (clusterOptions, childNodes, childEdges) {
                  let childrenCount = 0;
                  for (var j = 0; j < childNodes.length; j++) {
                    childrenCount += childNodes[j].childrenCount || 1;
                  }

                  clusterOptions.childrenCount = childrenCount;
                  clusterOptions.label = " (" + childrenCount + ")";
                  clusterOptions.id = clusterID;
                  clusterOptions.color = childNodes[0].color;

                  return clusterOptions;
                },
                joinCondition: function (childOptions) {
                  return (childOptions.hasOwnProperty('clusterID') &&
                    childOptions['clusterID'] === clusterID);
                },
                clusterNodeProperties: {borderWidth: 3, shape: 'box'}
              };

              this.network.cluster(clusterOptionsByData);
            }
        },
        expandClusters: function() {
          for (var i = 0; i < this.clusters.length; i++){
            this.network.openCluster(this.clusters[i]);
          }
        }
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

function findCluster(clusters, id){
  for (var i = 0; i < clusters.length; i++) {
    if (clusters[i].id === id) {
      return i;
    }
  }
  return null;
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

function getNodeHierarchy(node) {
  if (node.IssuingInstitution_Group in HIERARCHY)
    return HIERARCHY[node.IssuingInstitution_Group];
  else
    return HIERARCHY['Onbekend']
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
