import sys

sys.path.append('../../')
from webcrawler_plus.parser import crawl_feeds

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

if __name__ == '__main__':
    # crawl_feeds(
    #     settings=common_settings, feed_urls=['http://www.jimmunol.org/rss/current.xml', "https://blog.google/rss/"]
    # )

    crawl_feeds(
        settings=common_settings, feed_urls=['http://connect.iisc.ac.in/feed/',]
    )
