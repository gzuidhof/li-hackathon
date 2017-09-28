from flask import Flask, request, jsonify
from flask_cors import CORS
from neo4j.v1 import GraphDatabase, basic_auth

app = Flask(__name__)
CORS(app)


@app.route('/document')
def document():
    ecli = request.args.get('ecli')
    result = session.run('''
        MATCH (d:Document)-[r:REFERENCE]-(o:Document) WHERE d.SearchNumber={ecli}
        RETURN d, o, r
        ''',
        {'ecli': ecli}
    )
    docs = []
    references = []
    found_ids = set()
    for record in result:
        for doc in (record['d'], record['o']):
            doc_id = doc['id']
            if doc_id not in found_ids:
                found_ids.add(doc_id)
                docs.append(dict(doc))
        references.append({
            'from': record['d']['id'],
            'to': record['o']['id'],
            'count': record['r']['Count'],
        })

    return jsonify({
        'docs': docs,
        'references': references,
    })

if __name__ == '__main__':
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "joris"))
    session = driver.session()

    app.run(debug=True, use_reloader=True)