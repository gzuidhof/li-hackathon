from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
from flask_cors import CORS
from neo4j.v1 import GraphDatabase, basic_auth

app = Flask(__name__)
CORS(app)


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
    result = session.run(query
    )
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

    return jsonify({
        'docs': docs,
        'references': references,
    })

if __name__ == '__main__':
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "joris"))
    session = driver.session()

    app.run(host='0.0.0.0', port=6000, debug=True, use_reloader=True)

