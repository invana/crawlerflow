import sys

sys.path.append('../../')
from invana_bot.parser import crawl_website
import json

common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'LOG_LEVEL': 'INFO'
}

pipeline_settings = {
    'ITEM_PIPELINES': {'invana_bot.storages.elasticsearch.ElasticSearchPipeline': 1},
    'HTTPCACHE_STORAGE': "invana_bot.httpcache.elasticsearch.ESCacheStorage",
}

es_settings = {
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
common_settings.update(es_settings)
print(common_settings)

if __name__ == '__main__':
    crawl_website(url="https://medium.com/invanalabs",
                  settings=common_settings,
                  ignore_urls_with_words=['@'],
                  allow_only_with_words=['/invanalabs'],
                  )
