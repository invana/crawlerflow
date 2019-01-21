from invana_bot import InvanaBot

if __name__ == '__main__':
    crawler = InvanaBot(
        cache_database_uri="127.0.0.1",
        storage_database_uri="127.0.0.1",
        cache_database="mongodb",
        storage_database="mongodb",
    )
    crawler.crawl_feeds(
        feed_urls=[
            # 'http://connect.iisc.ac.in/feed/',
            # "https://blog.google/rss/",
            # "https://blog.github.com/all.atom",
            # "https://githubengineering.com/atom.xml",
            # "http://blog.atom.io/feed.xml",
            # "https://phraseapp.com/blog/feed/",
            # "https://blog.bitbucket.org/feed/",
            # "https://scienceblog.com/feed/",
            "http://www.jimmunol.org/rss/current.xml",
            "http://feeds.nature.com/gt/rss/current",
            "http://feeds.nature.com/gene/rss/current",
            "http://feeds.nature.com/gim/rss/current",
            "http://feeds.nature.com/npjqi/rss/current",
            "http://feeds.nature.com/npjquantmats/rss/current",
            "http://feeds.nature.com/npjregenmed/rss/current"
        ]
    )
