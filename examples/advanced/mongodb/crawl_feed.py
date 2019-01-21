import sys

sys.path.append('../../')
from invana_bot.parser import crawl_feeds

common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'LOG_LEVEL': 'INFO'
}

pipeline_settings = {
    'ITEM_PIPELINES': {'invana_bot.pipelines.mongodb.MongoDBPipeline': 1},
    'HTTPCACHE_STORAGE': "invana_bot.httpcache.mongodb.MongoDBCacheStorage",
}

mongodb_settings = {
    'INVANA_BOT_SETTINGS': {
        'HTTPCACHE_STORAGE_SETTINGS': {
            'DATABASE_URI': "mongodb://127.0.0.1",
            'DATABASE_NAME': "crawler_cache_db",
            'COLLECTION_NAME': "web_link",
            "EXPIRY_TIME": 3600
        },
        'ITEM_PIPELINES_SETTINGS': {
            'DATABASE_URI': "mongodb://127.0.0.1",
            'DATABASE_NAME': "crawler_data",
            'COLLECTION_NAME': "crawler_feeds_data"
        }
    }
}

common_settings.update(pipeline_settings)
common_settings.update(mongodb_settings)

if __name__ == '__main__':
    crawl_feeds(
        settings=common_settings, feed_urls=['http://connect.iisc.ac.in/feed/',
                                             "https://blog.google/rss/",
                                             "https://blog.github.com/all.atom",
                                             "https://githubengineering.com/atom.xml",
                                             "http://blog.atom.io/feed.xml",
                                             "https://phraseapp.com/blog/feed/",
                                             "https://blog.bitbucket.org/feed/",
                                             "https://scienceblog.com/feed/",
                                             "http://scienceblogs.com/feed/"
                                             "http://www.jimmunol.org/rss/current.xml",
                                             "http://feeds.nature.com/gt/rss/current",
                                             "http://feeds.nature.com/gene/rss/current",
                                             "http://feeds.nature.com/gim/rss/current",
                                             "http://feeds.nature.com/npjqi/rss/current",
                                             "http://feeds.nature.com/npjquantmats/rss/current",
                                             "http://feeds.nature.com/npjregenmed/rss/current"
                                             ]
    )
