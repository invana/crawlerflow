import pymongo
from webcrawler.settings import *
from datetime import datetime


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            MONGO_CONNECTION.get('MONGODB_SERVER'),
            MONGO_CONNECTION.get('MONGODB_PORT')
        )
        self.db = connection[MONGO_CONNECTION.get('MONGODB_DBNAME')]
        self.collection = self.db[MONGO_CONNECTION.get('MONGODB_COLLECTION')]

    def process_item(self, item, spider):
        if self.collection is None:
            raise Exception("self.connect() it not called in the Pipiline, please make the connection first")
        data = dict(item)
        data['updated_at'] = datetime.now()
        self.collection.insert(data)
        print("Post added to MongoDB")
        return item
