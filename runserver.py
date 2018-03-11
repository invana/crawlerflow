from webcrawler.utils import example_config
from webcrawler.parser import crawler
import pymongo
from datetime import datetime

MONGO_CONNECTION = {
    'MONGODB_SERVER': '127.0.0.1',
    'MONGODB_PORT': 27017,
    'MONGODB_DBNAME': 'test',
    'MONGODB_COLLECTION': 'crawled_data'
}


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

        items_keys = ['blogs', 'items', 'feeds']
        for key in items_keys:
            if key in data.keys():
                blogs = data.get(key, [])
                for blog in blogs:
                    data_ = dict(blog)
                    data_['updated_at'] = datetime.now()
                    self.db[key].insert(data_)
        print("Post added to MongoDB")
        return item


settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,

    'INVANA_CRAWLER_COLLECTION': "weblinks",
    'INVANA_CRAWLER_EXTRACTION_COLLECTION': "weblinks_extracted_data",

    # 'PIPELINE_MONGODB_DATABASE': "crawlers",
    # 'ITEM_PIPELINES': {'webcrawler.pipelines.mongodb.MongoDBPipeline': 1},

    # 'HTTPCACHE_STORAGE': "webcrawler.httpcache.mongodb.MongoDBCacheStorage",
    # 'HTTPCACHE_MONGODB_DATABASE': "crawlers",


    'HTTPCACHE_STORAGE': "webcrawler.httpcache.elasticsearch.ESCacheStorage",
    'HTTPCACHE_ES_DATABASE': "crawlers",
    "HTTPCACHE_MONGODB_PORT": 27017,

    'LOG_LEVEL': 'INFO'

}

if __name__ == '__main__':
    crawler(config=example_config, settings=settings)
