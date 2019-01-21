from invana_bot import InvanaBot

if __name__ == '__main__':
    crawler = InvanaBot(
        cache_database_uri="mongodb://127.0.0.1",
        storage_database_uri="mongodb://127.0.0.1",
        cache_database="mongodb",
        storage_database="mongodb",
    )
    crawler.run(urls=["https://medium.com/invanalabs", ],
                ignore_urls_with_words=['@'],
                allow_only_with_words=['/invanalabs'],
                )
