from invana_bot import InvanaBot

client_info = {
    "crawler_name": "scrapinghub-1",
    "domain": "scrapinghub.com",
    "subdomain": "blog.scrapinghub.com",
    "client_id": "invana",
    "crawler_pipeline_id": "11223"
}
if __name__ == '__main__':
    crawler = InvanaBot(
        cache_database_uri="mongodb://127.0.0.1",
        storage_database_uri="mongodb://127.0.0.1",
        cache_database="mongodb",
        storage_database="mongodb",
    )
    crawler.crawl_websites(urls=["https://blog.scrapinghub.com", ],
                           # ignore_urls_with_words=['@'],
                           # allow_only_with_words=['/invanalabs'],
                           context=client_info
                           )
