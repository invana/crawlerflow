import sys
sys.path.append('../../')
from invana_bot.parser import crawl_website
import json

example_config = json.load(open('../example.json'))
common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'CACHE_COLLECTION': "web_link",
    'INVANA_BOT_EXTRACTED_DATA_COLLECTION': "web_link_extracted_data",
    'LOG_LEVEL': 'INFO'
}

es_settings = {
    'ITEM_PIPELINES': {'invana_bot.pipelines.elasticsearch.ElasticsearchPipeline': 1},

    'HTTPCACHE_STORAGE': "invana_bot.httpcache.elasticsearch.ESCacheStorage",
}

common_settings.update(es_settings)
print(common_settings)

if __name__ == '__main__':
    crawl_website(url="https://medium.com/invanalabs",
                  settings=common_settings,
                  ignore_urls_with_words=['@'],
                  allow_only_with_words=['/invanalabs'],
                  )
