import sys

sys.path.append('../../')
from webcrawler.parser import crawl_website

common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'INVANA_CRAWLER_COLLECTION': "weblinks",
    'INVANA_CRAWLER_EXTRACTION_COLLECTION': "weblinks_extracted_data",
    'LOG_LEVEL': 'INFO'
}

solr_settings = {
    # 'ITEM_PIPELINES': {'webcrawler.pipelines.elasticsearch.ElasticsearchPipeline': 1},


    'HTTPCACHE_SOLR_HOST' : '127.0.0.1:8983',
    'HTTPCACHE_STORAGE': "webcrawler.httpcache.solr.SolrCacheStorage",
}

common_settings.update(solr_settings)

if __name__ == '__main__':
    crawl_website(url="https://blog.github.com/",
                  settings=common_settings, ignore_urls_with_words=['event', ])
