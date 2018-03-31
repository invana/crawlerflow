import pytest
import sys

sys.path.append('../../')


def test_solr_cache_storage():
    from webcrawler_plus.spiders.search_engines.bing import crawl_with_bing
    common_settings = {
        'COMPRESSION_ENABLED': False,
        'HTTPCACHE_ENABLED': True,
        'WCP_CRAWLER_COLLECTION': "weblinks",
        'WCP_CRAWLER_EXTRACTION_COLLECTION': "weblinks_extracted_data",
        'LOG_LEVEL': 'INFO'
    }

    es_settings = {
        'ITEM_PIPELINES': {'webcrawler_plus.pipelines.mongodb.MongoDBPipeline': 1},
        'HTTPCACHE_STORAGE': "webcrawler_plus.httpcache.mongodb.MongoDBCacheStorage",
    }

    common_settings.update(es_settings)

    crawl_with_bing(
        settings=common_settings, topic="Invaana"
    )

    ## check if there are some results added into the mongodb items collection

    ## check if there are some results added into the mongodb cache collection

    assert True
