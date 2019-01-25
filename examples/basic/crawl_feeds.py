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
            "https://blog.scrapinghub.com/rss.xml"
        ]
    )
