from datetime import datetime
from google.cloud import datastore
#from google.appengine.ext import ndb


class Capital:


    def __init__(self):
        self.ds = datastore.Client(project="hackathon-team-018")
        self.kind = "PythonCapital"
        self.data = {}

    
    def get_key(self, id):
        return self.ds.key(self.kind, id)


    def store_capital(self, uniqueid, obj):
        key = self.ds.key(self.kind, uniqueid)
        entity = datastore.Entity(key)

        entity['id'] = int(uniqueid)
        entity['location'] = datastore.Entity(key=self.ds.key('EmbeddedKind'))
        entity['location']['latitude'] = obj['location']['latitude']
        entity['location']['longitude'] = obj['location']['longitude']
        entity['country'] = obj['country']
        entity['name'] = obj['name']
        entity['countryCode'] = obj['countryCode']
        entity['continent'] = obj['continent']

        key = self.ds.put(entity)
        self.data[id] = key
        return key

    def fetch_capitals(self):
        query = self.ds.query(kind=self.kind)
        return self.get_query_results(query)

    def fetch_capitals(self, restrictions):
        query = self.ds.query(kind=self.kind)
        return self.get_query_results(query)

    def get_query_results(self, query):
        results = list()
        for entity in list(query.fetch()):
            results.append(dict(entity))
        return results

    def get_capital(self, id):
        query = self.ds.query(kind=self.kind)
        query.add_filter('id', '=', int(id))
        return self.get_query_results(query)

    def delete_capital(self, id):
        key = self.ds.key(self.kind, id)
        self.ds.delete(key)
