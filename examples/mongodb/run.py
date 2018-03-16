import sys
sys.path.append('../../')
from webcrawler.parser import crawl_website
import json

example_config = json.load(open('../example.json'))

common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'INVANA_CRAWLER_COLLECTION': "weblinks",
    'INVANA_CRAWLER_EXTRACTION_COLLECTION': "weblinks_extracted_data",
    'LOG_LEVEL': 'INFO'
}

mongodb_settings = {
    'PIPELINE_MONGODB_DATABASE': "crawler_data",
    'ITEM_PIPELINES': {'webcrawler.pipelines.mongodb.MongoDBPipeline': 1},

    'HTTPCACHE_STORAGE': "webcrawler.httpcache.mongodb.MongoDBCacheStorage",
    'HTTPCACHE_MONGODB_DATABASE': "crawler_data",
    "HTTPCACHE_MONGODB_PORT": 27017,
}

common_settings.update(mongodb_settings)

if __name__ == '__main__':
    crawl_website(url="https://medium.com/invanatech",
                  settings=common_settings,
                  ignore_urls_with_words=['@'],
                  allow_only_with_words=['/invanatech'],
                  )