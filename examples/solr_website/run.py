import sys
sys.path.append('../../')
from webcrawler_plus.parser import crawl_website

common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'WCP_CRAWLER_COLLECTION': "weblinks",
    'WCP_CRAWLER_EXTRACTION_COLLECTION': "weblinks_extracted_data",
    'LOG_LEVEL': 'INFO'
}

solr_settings = {
    'HTTPCACHE_HOST': '127.0.0.1:8983',
    'HTTPCACHE_STORAGE': "webcrawler_plus.httpcache.solr.SolrCacheStorage",

    'ITEM_PIPELINES': {'webcrawler_plus.pipelines.solr.SolrPipeline': 1},
    'PIPELINE_HOST': '127.0.0.1:8983',

}

common_settings.update(solr_settings)

if __name__ == '__main__':
    crawl_website(url="https://medium.com/invanatech",
                  settings=common_settings,
                  ignore_urls_with_words=['@'],
                  allow_only_with_words=['/invanatech'],
                  )
