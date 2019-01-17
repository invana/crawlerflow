import sys
sys.path.append('../../')
from invana_bot.parser import crawl_website

common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'INVANA_BOT_COLLECTION': "web_link",
    'INVANA_BOT_EXTRACTION_COLLECTION': "web_link_extracted_data",
    'LOG_LEVEL': 'INFO'
}

solr_settings = {
    'HTTPCACHE_HOST': '127.0.0.1',
    'HTTPCACHE_STORAGE': "invana_bot.httpcache.solr.SolrCacheStorage",
    'ITEM_PIPELINES': {'invana_bot.pipelines.solr.SolrPipeline': 1},
    'PIPELINE_HOST': '127.0.0.1:8983',

}

common_settings.update(solr_settings)

if __name__ == '__main__':
    crawl_website(url="https://medium.com/invanalabs",
                  settings=common_settings,
                  ignore_urls_with_words=['@'],
                  allow_only_with_words=['/invanalabs'],
                  )
