import pymongo
from datetime import datetime


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
        if auth.get('username'):
            self.db_client = pymongo.MongoClient(host, **auth)
        else:
            self.db_client = pymongo.MongoClient(host, )
        self.db = self.db_client[database]
        self.collection = self.db[collection]  # TODO - move this to settings ?

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('PIPELINE_MONGODB_HOST', '127.0.0.1'),
            database=crawler.settings.get('PIPELINE_MONGODB_DATABASE', 'crawler_data'),
            username=crawler.settings.get('PIPELINE_MONGODB_USERNAME', ''),
            password=crawler.settings.get('PIPELINE_MONGODB_PASSWORD', ''),
            port=crawler.settings.get('PIPELINE_MONGODB_PORT', 27017),
            collection=crawler.settings.get('INVANA_CRAWLER_EXTRACTION_COLLECTION', "weblinks"),
        )

    def process_item(self, item, spider):
        if self.collection is None:
            raise Exception("self.connect() it not called in the Pipeline, please make the connection first")
        data = dict(item)
        data['updated_at'] = datetime.now()
        self.collection.insert(data)
        print("Post added to MongoDB")
        return item
