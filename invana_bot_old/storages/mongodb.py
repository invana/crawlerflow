import pymongo
from datetime import datetime


class MongoDBPipeline(object):
    def __init__(self,
                 connection_uri=None,
                 database_name=None,
                 collection_name=None):
        # TODO - implement caching the db_clients specific to collection and database
        if None in [connection_uri, database_name, collection_name]:
            raise Exception("connection_uri, database_name, collection_name should be provided.")

        self.db_client = pymongo.MongoClient(connection_uri)
        self.db = self.db_client[database_name]
        self.collection = self.db[collection_name]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            connection_uri=crawler.settings.get('INVANA_BOT_SETTINGS').get('ITEM_PIPELINES_SETTINGS').get(
                'CONNECTION_URI', None),
            database_name=crawler.settings.get('INVANA_BOT_SETTINGS').get('ITEM_PIPELINES_SETTINGS').get(
                'DATABASE_NAME', None),
            collection_name=crawler.settings.get('INVANA_BOT_SETTINGS').get('ITEM_PIPELINES_SETTINGS').get(
                'COLLECTION_NAME', None),
        )

    def process_item(self, item, spider):
        if self.collection is None:
            raise Exception("pymongo.MongoClient() it not called in the Pipeline, please make the connection first")
        data = dict(item)
        data['updated'] = datetime.now()
        self.collection.insert(data)
        # print("Item added to Storage", data)
        return item
