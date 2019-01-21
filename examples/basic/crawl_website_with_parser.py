from invana_bot import InvanaBot
import json

example_config = json.load(open('../example.json'))
print("example_configexample_config", example_config)
if __name__ == '__main__':
    crawler = InvanaBot(
        cache_database_uri="mongodb://127.0.0.1",
        storage_database_uri="mongodb://127.0.0.1",
        cache_database="mongodb",
        storage_database="mongodb",
    )
    crawler.run(urls=["https://blog.scrapinghub.com", ],
                parser_config=example_config
                )
