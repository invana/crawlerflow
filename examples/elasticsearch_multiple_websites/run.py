import sys

sys.path.append('../../')
from webcrawler.parser import crawle_multiple_websites

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

if __name__ == '__main__':
    urls = ["https://www.blog.google/", "https://blog.scrapinghub.com/", "https://blog.github.com/"]
    crawle_multiple_websites(urls=urls,
                             settings=common_settings,

                             ignore_urls_with_words=['event', ])
