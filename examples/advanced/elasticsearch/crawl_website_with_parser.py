import sys

sys.path.append('../../')
from invana_bot.parser import crawler
import json

example_config = json.load(open('../example.json'))
common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'LOG_LEVEL': 'INFO'
}

pipeline_settings = {
    'ITEM_PIPELINES': {'invana_bot.pipelines.elasticsearch.ElasticSearchPipeline': 1},
    'HTTPCACHE_STORAGE': "invana_bot.httpcache.elasticsearch.ESCacheStorage",
}

mongodb_settings = {
    'INVANA_BOT_SETTINGS': {
        'HTTPCACHE_STORAGE_SETTINGS': {
            'DATABASE_URI': "127.0.0.1",
            'DATABASE_NAME': "crawler_cache_db",
            'COLLECTION_NAME': "web_link",
            "EXPIRY_TIME": 3600
        },
        'ITEM_PIPELINES_SETTINGS': {
            'DATABASE_URI': "127.0.0.1",
            'DATABASE_NAME': "crawler_data",
            'COLLECTION_NAME': "crawler_website_parsed_data"
        }
    }
}

common_settings.update(pipeline_settings)
common_settings.update(mongodb_settings)
print(common_settings)

if __name__ == '__main__':
    crawler(
        settings=common_settings, config=example_config
    )
