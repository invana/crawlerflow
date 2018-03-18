import sys

sys.path.append('../../')
from webcrawler.parser import crawl_feeds

common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'INVANA_CRAWLER_COLLECTION': "weblinks",
    'INVANA_CRAWLER_EXTRACTION_COLLECTION': "website_feeds",
    'LOG_LEVEL': 'INFO'
}

solr_settings = {
    'HTTPCACHE_HOST': '127.0.0.1:8983',
    'HTTPCACHE_STORAGE': "webcrawler.httpcache.solr.SolrCacheStorage",

    'ITEM_PIPELINES': {'webcrawler.pipelines.solr.SolrPipeline': 1},
    'PIPELINE_HOST': '127.0.0.1:8983',

}

common_settings.update(solr_settings)

if __name__ == '__main__':
    crawl_feeds(
        settings=common_settings, feed_urls=['http://connect.iisc.ac.in/feed/',
                                             "https://blog.google/rss/",
                                             "https://blog.github.com/all.atom",
                                             "https://githubengineering.com/atom.xml",
                                             "http://blog.atom.io/feed.xml",
                                             "https://phraseapp.com/blog/feed/"]
    )

