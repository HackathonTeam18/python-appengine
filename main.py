from flask import Flask, request
import json
from flask import jsonify
from crud import Capital
import logging
import utility
from google.cloud import pubsub
from storage import Storage


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
    data['query'] = False
    data['search'] = False
    data['pubsub'] = False
    data['storage'] = True
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
        data = obj[0]['body']
        return data, 200
    else:
        return "{\"code\":404,\"message\":\"not found\"}", 404


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


@app.route('/api/capitals/<id>/publish', methods=['POST'])
def api_publish(id):
    try:
        obj = request.get_json()
        topicName = obj['topic']

        capitalData = capital.get_capital(id)
        if len(capitalData) <= 0:
            return "Capital record not found", 404

        pubsub_client = pubsub.Client()
        topic = pubsub_client.topic(topicName)
        data = capitalData[0]['body'].encode('utf-8')
        message_id = topic.publish(data)
    except Exception as e:
        # swallow up exceptions
        logging.exception('Unexpected error')
        return "Unexpected error", 500

    return "success", 200


@app.route('/api/capitals/<id>/store', methods=['POST'])
def api_store_capital(id):
    data = capital.get_capital(id)
    if len(data) > 0:
        obj = request.get_json()
        bucket_name = obj['bucket']
        storage = Storage(bucket_name)
        storage.upload_blob(data[0]['body'], str(capital.get_key(id)))
        return jsonify("success"), 200
    else:
        return "{\"code\":404,\"message\":\"not found\"}", 404


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # Used for running locally
    app.run(host='127.0.0.1', port=8080, debug=True)