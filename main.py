from flask import Flask, request, Response, render_template
import json
from flask import jsonify
from crud import Capital
import logging
import utility
from google.cloud import pubsub
from storage import Storage
import urllib2 
import collections

app = Flask(__name__)
capital = Capital()

@app.route('/')
def main_page():
    capitals = capital.fetch_capitals()
    results = collections.OrderedDict()
    for item in capitals:
        results[item['country']] = item['name']

    if request.method == 'GET':
        return render_template('main.html', comment=None, results=results)

@app.route('/api/status')
def api_status():
    data = {}
    data['insert'] = True
    data['fetch'] = True
    data['delete'] = True
    data['list'] = True
    data['query'] = True
    data['search'] = True
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
    search_value = request.args.get('search')
    print query_values
    if query_values == ['None'] and search_value == None:
        data = capital.fetch_capitals()
    elif search_value == None:
        data = capital.fetch_capitals_query(query_values[0], query_values[1])
    else:
        data = capital.fetch_capitals_query("name", search_value)
        data.extend(capital.fetch_capitals_query("continent", search_value))
        data.extend(capital.fetch_capitals_query("country", search_value))
        

    return jsonify(data), 200


@app.route('/api/capitals/<id>/publish', methods=['POST'])
def api_publish(id):
    try:
        obj = request.get_json()
        logging.info("input = {}" .format(obj))
        topicName = obj['topic']
        capitalData = capital.get_capital(id)
        if len(capitalData) <= 0:
            return Response(response="{\"code\":404,\"message\":\"Capital record not found\"}", status=404, mimetype="application/json")
        
        myList = topicName.split("/")
        projectIndex = myList.index('projects') + 1
        logging.info("project index = {}" + projectIndex)
        projectName = myList[projectIndex]
        
        pubsub_client = pubsub.Client(project = projectName)
        #pubsub_client = pubsub.Client()
        #pubsub_client = pubsub.Client(project = 'the-depot')
        #topic = pubsub_client.topic(topicName)

        topic = pubsub_client.topic(myList[len(myList) - 1])
        data = json.dumps(capitalData[0]).encode('utf-8')
        message_id = topic.publish(data)
    except Exception as e:
        # swallow up exceptions
        logging.exception('Unexpected error')
        return Response(response="{\"code\":500,\"message\":\"Unexpected error\"}", status=500, mimetype="application/json")
    
    logging.info('message id: {}' .format(message_id))
    result = "messageId: {}" .format(message_id)
    return Response(response=result, status=200, mimetype="application/json")


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