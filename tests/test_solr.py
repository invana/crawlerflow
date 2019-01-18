import pytest
import sys

sys.path.append('../../')


def test_solr_cache_storage():
    from invana_bot.spiders.search_engines.bing import crawl_with_bing
    common_settings = {
        'COMPRESSION_ENABLED': False,
        'HTTPCACHE_ENABLED': True,
        'CACHE_COLLECTION': "web_link",
        'INVANA_BOT_EXTRACTED_DATA_COLLECTION': "web_link_extracted_data",
        'LOG_LEVEL': 'INFO'
    }

    es_settings = {
        'ITEM_PIPELINES': {'invana_bot.pipelines.mongodb.MongoDBPipeline': 1},
        'HTTPCACHE_STORAGE': "invana_bot.httpcache.mongodb.MongoDBCacheStorage",
    }

    common_settings.update(es_settings)

    crawl_with_bing(
        settings=common_settings, topic="Invana"
    )

    ## check if there are some results added into the mongodb items collection

    ## check if there are some results added into the mongodb cache collection

    assert True
