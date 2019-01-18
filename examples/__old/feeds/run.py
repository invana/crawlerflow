import sys

sys.path.append('../../')
from invana_bot.parser import crawl_feeds

common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'INVANA_BOT_WEB_LINK_COLLECTION': "web_link",
    'INVANA_BOT_EXTRACTED_DATA_COLLECTION': "web_link_extracted_data",
    'LOG_LEVEL': 'INFO'
}

es_settings = {
    'ITEM_PIPELINES': {'invana_bot.pipelines.mongodb.MongoDBPipeline': 1},
    'HTTPCACHE_STORAGE': "invana_bot.httpcache.mongodb.MongoDBCacheStorage",
}

common_settings.update(es_settings)

if __name__ == '__main__':
    # crawl_feeds(
    #     settings=common_settings, feed_urls=['http://www.jimmunol.org/rss/current.xml', "https://blog.google/rss/"]
    # )
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

    # crawl_feeds(
    #     settings=common_settings, feed_urls=['http://connect.iisc.ac.in/feed/', ]
    # )
