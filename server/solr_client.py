import pysolr
from solr_parser import SolrParser
import pprint
import sys

solr = pysolr.Solr('http://94.198.25.91:8080/solr/ACC_Legal_Slave', search_handler='/tvrh', results_cls=dict)
solr_parser = SolrParser()


def get_backwards_references(ecli, id, rows=100):
    query = '{!raw f=Text_Text_2}' + f'{ecli}'

    print('=======BACKWARDS QUERY=======')
    print(query)
    result = solr.search(query, wt='json', rows=rows)
    docs, _ = solr_parser.parse_solr_response(result, forward_references=False)
    # Remove self-references
    docs = [d for d in docs if d['id'] != id]
    edges = [{'from': r['id'], 'to': id, 'count':1} for r in docs]
    print("=======BACKWARDS DOCUMENTS=======")
    pprint.pprint(docs, depth=2)
    return docs, edges


def get_documents(search_numbers, get_forward_references=True, get_backward_references=True, rows=100):
    if len(search_numbers) == 1:
        query = '{!raw f=SearchNumbers}' + f'{search_numbers[0]}'
    else:
        query = ' OR '.join(['({!raw f=SearchNumbers}' + sn + ')' for sn in search_numbers])
    print("=======QUERY=======")
    print(query)
    result = solr.search(query, wt='json', rows=rows)
    docs, forward_references = solr_parser.parse_solr_response(result, forward_references=get_forward_references)

    all_docs = docs.copy()

    doc_ids = [d['id'] for d in docs]
    edges = []

    if get_forward_references:
        for original_doc, forward_search_numbers in zip(docs, forward_references):
            # Remove self-references
            forward_search_numbers = [sn for sn in forward_search_numbers if sn != original_doc['SearchNumber']]
            docs_forward, _ = get_documents(forward_search_numbers, get_forward_references=False,
                                            get_backward_references=False)

            # Add edges
            new_edges = [{'from': original_doc['id'], 'to': d['id'], 'count': 1} for d in docs_forward]
            edges.extend(new_edges)

            # Add docs (only those that weren't already added in previous steps)
            docs_forward = [d for d in docs_forward if d not in doc_ids]
            all_docs.extend(docs_forward)
            doc_ids.extend([d['id'] for d in docs_forward])

    if get_backward_references:
        for original_doc in docs:
            docs_back, edges_back = get_backwards_references(original_doc['SearchNumber'], original_doc['id'])
            doc_ids.extend([d['id'] for d in docs_back])
            all_docs.extend(docs_back)
            edges.extend(edges_back)

    print("=======ALL DOCUMENTS=======")
    pprint.pprint(all_docs, depth=2)
    print("=======REFERENCES=======")
    pprint.pprint(edges)
    return all_docs, edges


if __name__ == '__main__':
    get_documents(['ECLI:NL:PHR:2016:987'])
