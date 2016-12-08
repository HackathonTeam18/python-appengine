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


    def store_capital(self, uniqueid, body):
        key = self.ds.key(self.kind, uniqueid)
        entity = datastore.Entity(key)

        entity['id'] = uniqueid
        entity['body'] = body
        key = self.ds.put(entity)
        self.data[id] = key
        return key

    def fetch_capitals(self):
        query = self.ds.query(kind=self.kind)
        return self.get_query_results(query)
    

    def fetch_capitals_query(self, prop, val):
        query = self.ds.query(kind=self.kind)
        query.add_filter(prop, "=", val)
        return self.get_query_results(query)

    
    def get_query_results(self, query):
        results = list()
        for entity in list(query.fetch()):
            results.append(dict(entity))
        return results


    def get_capital(self, id):
        query = self.ds.query(kind=self.kind)
        query.add_filter('id', '=', id)
        return self.get_query_results(query)

    def delete_capital(self, id):
        #query = self.ds.query(kind=self.kind)
        #query.add_filter('id', '=', id)
        #obj = self.get_query_results(query)
        #print obj.key()
        #results = query.fetch()
        #print "results:"
        #print results.key()
        #key = self.ds.key(self.kind)
        #entity = datastore.Entity(key)
        #entity['id'] = id
        #result = self.ds.get(entity)
        #result.delete()
        key = self.ds.key(self.kind, id)
        self.ds.delete(key)
