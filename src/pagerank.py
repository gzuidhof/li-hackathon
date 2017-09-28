import networkx as nx
import pandas as pd
from tqdm import tqdm

def create_graph():
    documents = pd.read_csv('~/neo4j-community-3.2.5/import/documents.csv', usecols=['ID', 'PublicationNumber', 'SearchNumber'])
    # laws = pd.read_csv('~/neo4j-community-3.2.5/import/wetboekenteksten.csv', usecols=['link'])
    references = pd.read_csv('~/neo4j-community-3.2.5/import/references.csv', usecols=['ID', 'References'])
    # law_references = pd.read_csv('~/neo4j-community-3.2.5/import/law_references.csv', usecols=['ID', 'wetboeklink'])
    sn_to_id = {sn: id for id, _, sn in documents.itertuples(index=False)}
    graph = nx.Graph()
    graph.add_nodes_from(documents.ID)
    for id, ref in tqdm(references.itertuples(index=False), total=len(references)):
        if ref in sn_to_id:
            id2 = sn_to_id[ref]
            graph.add_edge(id, id2)
    

    nx.write_gpickle(graph, 'graph.pkl')

def do_pagerank():
    graph = nx.read_gpickle('graph.pkl')
    print('Doing pagerank...')
    ranks = nx.pagerank(graph)
    with open('pagerank.csv', 'w') as f:
        f.write('id,pagerank\n')
        for id, rank in tqdm(ranks.items()):
            f.write('{},{}\n'.format(id, rank))

if __name__ == '__main__':
    create_graph()
    do_pagerank()