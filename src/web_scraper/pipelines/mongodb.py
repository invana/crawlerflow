import pymongo
import logging


class MongoDBPipeline(object):

    def __init__(self, mongo_uri, mongo_db, default_collection_name = None ):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.default_collection_name = default_collection_name
        self.client = None
        self.db = None
        

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings.get("STORAGE_MONGO_URI"),
            crawler.settings.get("STORAGE_MONGO_DATABASE"),
            default_collection_name = crawler.settings["STORAGE_MONGO_DEFAULT_COLLECTION"]            
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    @property
    def default_collection(self):
        return self.db[self.default_collection_name]

    def process_item(self, item, spider):
        meta__scraper_name =  item.get("meta__scraper_name")
        collection = self.db[meta__scraper_name] if meta__scraper_name else self.default_collection
        collection.insert_one(item)        
        logging.debug("Item added to MongoDB database!")
        return item
 