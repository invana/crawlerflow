from __future__ import unicode_literals
from pymongo import MongoClient
from invana_bot.transformers.executors import Executor
from datetime import datetime


class WriteToMongoDB(Executor):
    def __init__(self, connection_string, db, collection, unique_key, docs=None, update=True):
        self._connection_string = connection_string
        self._db = db
        self._collection = collection
        self._docs = docs
        self._unique_key = unique_key

    def connect(self):
        self._client = MongoClient(self._connection_string)

    def get_object(self, doc=None):
        return self._client[self._db][self._collection].find_one({self._unique_key: doc.get(self._unique_key)})

    def write(self):

        if isinstance(self._client, MongoClient):
            for doc in self._docs:
                entry = self.get_object(doc=doc)
                print("Writing the document ::{} with keys".format(doc.keys()))
                if entry is None:
                    self._client[self._db][self._collection].insert(doc)
                else:
                    doc['updated'] = datetime.now()
                    self._client[self._db][self._collection].update_one({self._unique_key: doc.get(self._unique_key)},
                                                                        {"$set": doc})

    def disconnect(self):
        if isinstance(self._client, MongoClient):
            self._client.close()


class ReadFromMongo(Executor):
    def __init__(self, connection_string, db, collection, query=None, fields=None):
        self._connection_string = connection_string
        self._db = db
        self._collection = collection
        self._query = query
        self._fields = fields
        self._client = None

    def connect(self):
        self._client = MongoClient(self._connection_string)

    def read(self):
        if isinstance(self._client, MongoClient):
            for doc in self._client[self._db][self._collection].find(self._query, projection=self._fields):
                yield doc

    def disconnect(self):
        if isinstance(self._client, MongoClient):
            self._client.close()


class OTManager(object):
    """
        Object Transform Manager Renders the output into required form
        Arguments
        ---------
        ops - list of OTConf objects
    """

    def __init__(self, ops):
        self._ops = ops
        self.results = []

    def _sub_process(self, op, _object):
        if op.key_path in _object:
            op.cls(op.key_path, *op.args, **op.kwargs).process(_object)
        elif '.' in op.key_path:
            key_split = op.key_path.split('.')
            _op = op.clone()
            _op.key_path = '.'.join(key_split[1:])
            if isinstance(_object[key_split[0]], list):
                for _list_item in _object[key_split[0]]:
                    self._sub_process(_op, _list_item)
            else:
                self._sub_process(_op, _object[key_split[0]])
        return _object

    def process(self, executor):
        for _object in executor.read():
            for op in self._ops:
                self._sub_process(op, _object)
            self.results.append(_object)
        return self
