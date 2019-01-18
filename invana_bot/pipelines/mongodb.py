import pymongo
from datetime import datetime
from invana_bot.settings import DATABASE


class MongoDBPipeline(object):
    def __init__(self,
                 database_uri=None,
                 database_name=None,
                 collection_name=None):
        self.db_client = pymongo.MongoClient(database_uri)
        self.db = self.db_client[database_name]
        self.collection = self.db[collection_name]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database_uri=crawler.settings.get('INVANA_BOT_SETTINGS').get('ITEM_PIPELINES_SETTINGS').get('DATABASE_URI',
                                                                                                        DATABASE),
            database_name=crawler.settings.get('INVANA_BOT_SETTINGS').get('ITEM_PIPELINES_SETTINGS').get(
                'DATABASE_NAME', DATABASE),
            collection_name=crawler.settings.get('INVANA_BOT_SETTINGS').get('ITEM_PIPELINES_SETTINGS').get(
                'DATABASE_COLLECTION', DATABASE),
        )

    def process_item(self, item, spider):
        if self.collection is None:
            raise Exception("pymongo.MongoClient() it not called in the Pipeline, please make the connection first")
        data = dict(item)
        data['updated'] = datetime.now()
        self.collection.insert(data)
        print("Post added to MongoDB")
        return item
