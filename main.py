from flask import Flask
import json
from flask import jsonify


app = Flask(__name__)


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
    data = json.dumps({'insert':'false','fetch':'false', 'delete': 'false',  'list': 'false'})
    return data


@app.route('/api/capitals/<id>', methods=['GET'])
def api_get(id):
    data = json.dumps({'insert':'false','fetch':'false', 'delete': 'false',  'list': 'false'})
    return data


@app.route('/api/capitals/<id>', methods=['PUT'])
def api_update(id):
    data = json.dumps({'insert':'false','fetch':'false', 'delete': 'false',  'list': 'false'})
    return data


@app.route('/api/capitals', methods=['GET'])
def api_list():
    data = json.dumps({'insert':'false','fetch':'false', 'delete': 'false',  'list': 'false'})
    return data


if __name__ == '__main__':
    # Used for running locally
    app.run(host='127.0.0.1', port=8080, debug=True)