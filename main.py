from flask import Flask, request, Response
import json
from flask import jsonify
from crud import Capital
import logging
import utility
from google.cloud import pubsub
from storage import Storage
import urllib2 


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
    data['query'] = True
    data['search'] = False
    data['pubsub'] = True
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
        return Response(response=json.dumps(obj[0]), status=200, mimetype="application/json")
    else:
        return Response(response="{\"code\":404,\"message\":\"not found\"}", status=404, mimetype="application/json")


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

    capital.store_capital(id, obj)
    return "success", 200


@app.route('/api/capitals', methods=['GET'])
def api_list():
    query_values = str(request.args.get('query')).split(":")
    if query_values == ['None']:
        data = capital.fetch_capitals()
    else:
        data = capital.fetch_capitals_query(query_values[0], query_values[1])

    return jsonify(data), 200


@app.route('/api/capitals/<id>/publish', methods=['POST'])
def api_publish(id):
    try:
        obj = request.get_json()
        topicName = obj['topic']
        capitalData = capital.get_capital(id)
        if len(capitalData) <= 0:
            return "Capital record not found", 404
        
        myList = topicName.split("/")
        pubsub_client = pubsub.Client(project='the-depot')
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
    try:
        data = capital.get_capital(id)
        if len(data) > 0:
            obj = request.get_json()
            bucket_name = obj['bucket']
            logging.info("bucket name is {}".format(bucket_name))
            storage = Storage(bucket_name)
            storage.upload_blob(json.dumps(data[0]), str(id))
            return jsonify("success"), 200
        else:
            return Response(response="{\"code\":404,\"message\":\"not found\"}", status=404, mimetype="application/json")

            #except urllib2.HTTPError, err:
    except Exception as err:
        return Response(response="{\"code\":500,\"message\":\"Unexpected error\"}", status=500, mimetype="application/json")


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