import sys

sys.path.append('../../')
from webcrawler_plus.parser import crawler
import json

example_config = json.load(open('../example.json'))
common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': False,
    'WCP_CRAWLER_COLLECTION': "weblinks",
    'WCP_CRAWLER_EXTRACTION_COLLECTION': "weblinks_extracted_data",
    'LOG_LEVEL': 'INFO'
}

es_settings = {
    'ITEM_PIPELINES': {'webcrawler_plus.pipelines.mongodb.MongoDBPipeline': 1},

    'HTTPCACHE_STORAGE': "webcrawler_plus.httpcache.mongodb.MongoDBCacheStorage",
}

common_settings.update(es_settings)
print(common_settings)

if __name__ == '__main__':
    crawler(
        settings=common_settings, config=example_config
    )
