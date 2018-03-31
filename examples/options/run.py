import sys

sys.path.append('../../')
from webcrawler_plus.options import WebCrawlerPlus

if __name__ == '__main__':
    crawler = WebCrawlerPlus(
        database_credentials={
            "database": "crawler_test"
        },
        database="mongodb",
    )
    crawler.run(urls=["https://medium.com/invanatech", ],
                ignore_urls_with_words=['@'],
                allow_only_with_words=['/invanatech'],
                )
