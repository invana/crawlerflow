# Web Crawler Plust

A micro-framework built on [scrapy](https://scrapy.org/) to crawl the sites. 
It can use [MongoDB](https://www.mongodb.com/), [Elasticsearch](https://www.elastic.co/products/elasticsearch) 
and [Solr](http://lucene.apache.org/solr/) databases to cache the requests and also extract the data using parser configs 
and save them.


[![Build Status](https://travis-ci.org/invanatech/web-crawler-plus.svg?branch=master)](https://travis-ci.org/invanatech/web-crawler-plus) 
[![codecov](https://codecov.io/gh/invanatech/web-crawler-plus/branch/master/graph/badge.svg)](https://codecov.io/gh/invanatech/web-crawler-plus) 

## Install

```bash

pip install web-crawler-plus

```



```python
# a simple usecase to use mongodb as cache and storage db.

from webcrawler_plus.options import WebCrawlerPlus

if __name__ == '__main__':
    crawler = WebCrawlerPlus(
        database_credentials={
            "database": "crawler_test",
            "host": "127.0.0.1",
            "port": "27017",
        },
        database="mongodb",
    )
    crawler.run(urls=["https://medium.com/invanatech", ],
                ignore_urls_with_words=['@'],
                allow_only_with_words=['/invanatech'],
                )


```

```python
# a simple usecase to use solr as cache and storage db.

from webcrawler_plus.options import WebCrawlerPlus

if __name__ == '__main__':
    # there is no database key for solr, it will be ignored
    crawler = WebCrawlerPlus(
        database_credentials={
            "host": "127.0.0.1",
            "port": "8983",
        },
        database="solr",
    )
    crawler.run(urls=["https://medium.com/invanatech", ],
                ignore_urls_with_words=['@'],
                allow_only_with_words=['/invanatech'],
                )


```

```python
# a simple usecase to use elasticsearch as cache and storage db.

from webcrawler_plus.options import WebCrawlerPlus

if __name__ == '__main__':
    crawler = WebCrawlerPlus(
        database_credentials={
            "host": "127.0.0.1",
            "port": "9200",
        },
        database="elasticsearch",
    )
    crawler.run(urls=["https://medium.com/invanatech", ],
                ignore_urls_with_words=['@'],
                allow_only_with_words=['/invanatech'],
                )


```

Checkout the lower level [documentation](docs/index.md) for more information.
