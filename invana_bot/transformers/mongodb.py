from __future__ import unicode_literals
from pymongo import MongoClient
from transformers.executors import Executor
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
                print("Writing the document ::{}".format(doc))
                if entry is None:
                    self._client[self._db][self._collection].insert(doc)
                else:
                    doc['updated'] = datetime.now()
                    self._client[self._db][self._collection].update_one({self._unique_key: doc.get(self._unique_key)},
                                                                        {"$set": doc})

    def disconnect(self):
        if isinstance(self._client, MongoClient):
            self._client.close()
