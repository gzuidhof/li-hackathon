import pprint

import pysolr
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.exceptions import BadRequest

from solr_client import get_documents
from solr_parser import SolrParser

app = Flask(__name__)
CORS(app)


@app.route('/solrdocument')
@cross_origin(supports_credentials=True)
def solrdocument():
    ecli = request.args.get('ecli')
    depth = request.args.get('depth', 2)
    id = request.args.get('id')
    mode = request.args.get('mode', 'referenties')

    if ecli is not None:
        print("Requesting " + ecli)
    if id is not None:
        print("Requesting id " + id)

    docs, references = get_documents([ecli])

    return jsonify({
        'docs': docs,
        'references': references
    })


@app.route('/document')
def document():
    ecli = request.args.get('ecli')
    depth = request.args.get('depth', 2)
    id = request.args.get('id')
    mode = request.args.get('mode', 'referenties')
    where_clause = 'WHERE '
    if ecli:
        where_clause += f'd.SearchNumber="{ecli}",'
    if id:
        where_clause += f'd.id={id},'
    where_clause = where_clause[:-1] + ' '
    if mode == 'referenties':
        query = (
            f'MATCH (d)-[r*..{depth}]-(o)' +
            where_clause +
            'AND all(x in r WHERE type(x) = "REFERENCE" OR type(x) = "LAW_REFERENCE")' + 
            'RETURN DISTINCT([d] + o) as nodes, r'
        )
    elif mode == 'clicks':
        query = (
            f'MATCH (d)-[r*..{depth}]-(o)' +
            where_clause +
            'AND all(x in r WHERE type(x) = "ALSO_VIEWED")' + 
            'RETURN DISTINCT([d] + o) as nodes, r'
        )
    else:
        raise BadRequest('Unknown mode '+mode)
    print(query)
    result = session.run(query)
    docs = []
    references = []
    neo4j_id_to_doc_id = {}
    refs = []
    for record in result:
        for doc in record['nodes']:
            doc_id = doc.id
            if 'id' not in doc:
                id = hash(doc_id)
            else:
                id = doc['id']
            if doc_id not in neo4j_id_to_doc_id:
                neo4j_id_to_doc_id[doc.id] = id
                docs.append(dict(doc, id=id))
        for ref in record['r']:
            refs.append(ref)
    
    found_refs = set()
    for ref in refs:
        ref_id = str(ref.start)+str(ref.end)
        if ref_id not in found_refs:
            found_refs.add(ref_id)
            references.append({
                'from': neo4j_id_to_doc_id[ref.start],
                'to': neo4j_id_to_doc_id[ref.end],
                    'count': ref.get('Count'),
            })

    res = jsonify({
        'docs' : docs,
        'references' : references
    })
    print("=======DOCUMENTS=======")
    pprint.pprint(docs[0])
    print("=======REFERENCES=======")
    print(references)

    return res


if __name__ == '__main__':
    solr = pysolr.Solr('http://94.198.25.91:8080/solr/ACC_Legal_Slave', search_handler='/tvrh', results_cls=dict)
    solr_parser = SolrParser()

    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)

