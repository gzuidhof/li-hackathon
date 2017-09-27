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
        RETURN d, o
        ''',
        {'ecli': ecli}
    )
    links = {}
    docs = []
    for record in result:
        doc_id = record['d']['id']
        if doc_id in links:
            links[doc_id].append(dict(record['o']))
        else:
            docs.append(dict(record['d']))
            links[doc_id] = [dict(record['o'])]

    return jsonify([{
            'document': d,
            'links': [l for l in links[d['id']]]
    } for d in docs])

if __name__ == '__main__':
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "joris"))
    session = driver.session()

    app.run(debug=True, use_reloader=True)