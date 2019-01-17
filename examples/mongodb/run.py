import sys
sys.path.append('../../')
from invana_bot.parser import crawl_website
import json

example_config = json.load(open('../example.json'))

common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'INVANA_BOT_COLLECTION': "web_link",
    'INVANA_BOT_EXTRACTION_COLLECTION': "web_link_extracted_data",
    'LOG_LEVEL': 'INFO'
}

mongodb_settings = {
    'PIPELINE_MONGODB_DATABASE': "crawler_data",
    'ITEM_PIPELINES': {'invana_bot.pipelines.mongodb.MongoDBPipeline': 1},

    'HTTPCACHE_STORAGE': "invana_bot.httpcache.mongodb.MongoDBCacheStorage",
    "HTTPCACHE_MONGODB_PORT": 27017,
}

common_settings.update(mongodb_settings)

if __name__ == '__main__':
    crawl_website(url="https://medium.com/invanalabs",
                  settings=common_settings,
                  ignore_urls_with_words=['@'],
                  allow_only_with_words=['/invanalabs'],
                  )