import pymongo
from datetime import datetime
from webcrawler.settings import EXTRACTED_DATA_COLLECTION, DATABASE


class MongoDBPipeline(object):
    def __init__(self, host=None,
                 database=None,
                 username=None,
                 password=None,
                 port=None,
                 collection=None):

        auth = {
            "username": username,
            "password": password
        }
        if port:
            auth.update({"port": port})
        if auth.get('username'):
            self.db_client = pymongo.MongoClient(host, **auth)
        else:
            self.db_client = pymongo.MongoClient(host, )
        self.db = self.db_client[database]
        self.extracted_data_collection = self.db[collection]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('HTTPCACHE_HOST', '127.0.0.1'),
            database=crawler.settings.get('PIPELINE_MONGODB_DATABASE', DATABASE),
            username=crawler.settings.get('PIPELINE_MONGODB_USERNAME', ''),
            password=crawler.settings.get('PIPELINE_MONGODB_PASSWORD', ''),
            port=crawler.settings.get('PIPELINE_MONGODB_PORT', 27017),
            collection=crawler.settings.get('INVANA_CRAWLER_EXTRACTION_COLLECTION', EXTRACTED_DATA_COLLECTION),
        )

    def process_item(self, item, spider):

        if self.extracted_data_collection is None:
            raise Exception("pymongo.MongoClient() it not called in the Pipeline, please make the connection first")
        data = dict(item)
        data['updated'] = datetime.now()
        self.extracted_data_collection.insert(data)
        print("Post added to MongoDB")
        return item
