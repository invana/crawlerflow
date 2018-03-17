import sys

sys.path.append('../../')
from webcrawler.spiders.search_engines.bing import crawl_with_bing
import json

example_config = json.load(open('../example.json'))
common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': False,
    'INVANA_CRAWLER_COLLECTION': "weblinks",
    'INVANA_CRAWLER_EXTRACTION_COLLECTION': "weblinks_extracted_data",
    'LOG_LEVEL': 'INFO'
}

es_settings = {
    'ITEM_PIPELINES': {'webcrawler.pipelines.mongodb.MongoDBPipeline': 1},

    'HTTPCACHE_STORAGE': "webcrawler.httpcache.mongodb.MongoDBCacheStorage",
}

common_settings.update(es_settings)
print(common_settings)

if __name__ == '__main__':
    crawl_with_bing(
        settings=common_settings, topic="Invaana"
    )
