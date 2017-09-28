from flask import Flask, request, jsonify
from flask_cors import CORS
from neo4j.v1 import GraphDatabase, basic_auth

app = Flask(__name__)
CORS(app)


@app.route('/document')
def document():
    ecli = request.args.get('ecli')
    depth = request.args.get('depth', 2)
    id = request.args.get('id')
    where_clause = 'WHERE '
    if ecli:
        where_clause += f'd.SearchNumber="{ecli}",'
    if id:
        where_clause += f'd.id={id},'
    where_clause = where_clause[:-1] + ' '
    query = (
        f'MATCH (d:Document)-[r:REFERENCE*..{depth}]-(o:Document)' +
        where_clause +
        'RETURN DISTINCT([d] + o) as nodes, r'
    )
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
            if doc_id not in neo4j_id_to_doc_id:
                neo4j_id_to_doc_id[doc.id] = doc['id']
                docs.append(dict(doc))
        for ref in record['r']:
            refs.append(ref)
    
    found_refs = set()
    for ref in refs:
        if ref.id not in found_refs:
            found_refs.add(ref.id)
            references.append({
                'from': neo4j_id_to_doc_id[ref.start],
                'to': neo4j_id_to_doc_id[ref.end],
                'count': ref['Count'],
            })

    return jsonify({
        'docs': docs,
        'references': references,
    })

if __name__ == '__main__':
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "joris"))
    session = driver.session()

    app.run(host='0.0.0.0', debug=True, use_reloader=True)