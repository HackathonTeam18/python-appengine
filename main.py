from flask import Flask, request
import json
from flask import jsonify
from crud import Capital
import logging
import utility


app = Flask(__name__)
capital = Capital()


@app.route('/')
def hello_world():
    """hello world"""
    return 'Hello World!'

@app.route('/api/status')
def api_status():
    data = {}
    data['insert'] = True
    data['fetch'] = True
    data['delete'] = True
    data['list'] = True
    obj = jsonify(data)
    return obj, 200


@app.route('/api/capitals/<id>', methods=['DELETE'])
def api_delete(id):
    items = capital.get_capital(id)
    if len(items) > 0:
        capital.delete_capital(id)
        return "success", 200
    else:
        return "not found", 404



@app.route('/api/capitals/<id>', methods=['GET'])
def api_get(id):
    obj = capital.get_capital(id)
    if len(obj) > 0:
        data = jsonify(obj)
        return data, 200
    else:
        return "not found", 404


@app.route('/api/capitals/<id>', methods=['PUT'])
def api_update(id):
    data = {}
    returnMessage = ""
    try:
        obj = request.get_json()

    except Exception as e:
        # swallow up exceptions
        logging.exception('Oops!')
        return "exception"

    capital.store_capital(id, json.dumps(obj))
    return "success", 200


@app.route('/api/capitals', methods=['GET'])
def api_list():
    data = capital.fetch_capitals()
    return jsonify(data), 200


if __name__ == '__main__':
    # Used for running locally
    app.run(host='127.0.0.1', port=8080, debug=True)