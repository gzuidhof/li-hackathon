from flask import Flask, request, jsonify
from flask_cors import CORS
from neo4j.v1 import GraphDatabase, basic_auth

app = Flask(__name__)
CORS(app)


@app.route('/document')
def document():
    ecli = request.args.get('ecli')
    result = session.run('''
        MATCH (d:Document) WHERE d.SearchNumber = {ecli}
        RETURN d
        ''',
        {'ecli': ecli}
    )
    for record in result:
        return jsonify(dict(record['d']))

if __name__ == '__main__':
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "joris"))
    session = driver.session()

    app.run(debug=True, use_reloader=True)