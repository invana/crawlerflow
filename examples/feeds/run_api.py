import sys

sys.path.append('../../')
from webcrawler_plus.parser import crawl_feeds

common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'WCP_PIPELINE_API_URL': "http://localhost:8000/extracted-data",
    'WCP_PIPELINE_API_HEADERS':  {},
    'LOG_LEVEL': 'INFO'
}

es_settings = {
    'ITEM_PIPELINES': {'webcrawler_plus.pipelines.api.ApiPipeline': 1},

    'HTTPCACHE_STORAGE': "webcrawler_plus.httpcache.mongodb.MongoDBCacheStorage",
}

common_settings.update(es_settings)

if __name__ == '__main__':
    # crawl_feeds(
    #     settings=common_settings, feed_urls=['http://www.jimmunol.org/rss/current.xml',
    # 'http://connect.iisc.ac.in/feed/', "https://blog.google/rss/"]
    # )

    crawl_feeds(
        settings=common_settings, feed_urls=["https://blog.google/rss/"]
    )
