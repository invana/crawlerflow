import sys

sys.path.append('../../')
from invana_bot import InvanaBot

if __name__ == '__main__':
    crawler = InvanaBot(
        database_credentials={
            "database": "crawler_test"
        },
        database="mongodb",
    )
    crawler.run(urls=["https://medium.com/invanalabs", ],
                ignore_urls_with_words=['@'],
                allow_only_with_words=['/invanalabs'],
                )
