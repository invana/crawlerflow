import sys

sys.path.append('../../')

from webcrawler.parser import crawler, crawl_website
import json

example_config = json.load(open('../example.json'))
common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'INVANA_CRAWLER_COLLECTION': "weblinks",
    'INVANA_CRAWLER_EXTRACTION_COLLECTION': "weblinks_extracted_data",
    'LOG_LEVEL': 'INFO'
}

es_settings = {
    'ITEM_PIPELINES': {'webcrawler.pipelines.elasticsearch.ElasticsearchPipeline': 1},

    'HTTPCACHE_STORAGE': "webcrawler.httpcache.elasticsearch.ESCacheStorage",
}

common_settings.update(es_settings)
print(common_settings)

if __name__ == '__main__':
    crawl_website(url="http://www.srmuniv.ac.in/", settings=common_settings)
