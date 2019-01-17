import sys

sys.path.append('../../')
from invana_bot.spiders.search_engines.bing import crawl_with_bing
import json

example_config = json.load(open('../example.json'))
common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'INVANA_BOT_COLLECTION': "web_link",
    'INVANA_BOT_EXTRACTION_COLLECTION': "web_link_extracted_data",
    'LOG_LEVEL': 'INFO'
}

es_settings = {
    'ITEM_PIPELINES': {'invana_bot.pipelines.mongodb.MongoDBPipeline': 1},

    'HTTPCACHE_STORAGE': "invana_bot.httpcache.mongodb.MongoDBCacheStorage",
}

common_settings.update(es_settings)
print(common_settings)

if __name__ == '__main__':
    crawl_with_bing(
        settings=common_settings, topic="Invana"
    )
