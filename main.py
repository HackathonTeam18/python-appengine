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
    data = json.dumps({'insert':'false','fetch':'false', 'delete': 'false',  'list': 'false'})
    return data


@app.route('/api/capitals/<id>', methods=['DELETE'])
def api_delete(id):
    capital.delete_capital(id)
    return "200"


@app.route('/api/capitals/<id>', methods=['GET'])
def api_get(id):
    obj = capital.get_capital(id)
    data = jsonify(obj)
    return data


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
    return jsonify(data), 200


@app.route('/api/capitals', methods=['GET'])
def api_list():
    data = capital.fetch_capitals()
    return jsonify(data)


if __name__ == '__main__':
    # Used for running locally
    app.run(host='127.0.0.1', port=8080, debug=True)