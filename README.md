# Invana Bott

A micro-framework built on [scrapy](https://scrapy.org/) for crawling and 
storing to NoSQL database solutions. 

It can use [MongoDB](https://www.mongodb.com/), [Elasticsearch](https://www.elastic.co/products/elasticsearch) 
and <del>[Solr](http://lucene.apache.org/solr/)</del> databases to cache the requests and also extract the data using parser configs 
and save them.


[![Build Status](https://travis-ci.org/invanalabs/web-crawler-plus.svg?branch=master)](https://travis-ci.org/invanalabs/web-crawler-plus) 
[![codecov](https://codecov.io/gh/invanalabs/web-crawler-plus/branch/master/graph/badge.svg)](https://codecov.io/gh/invanalabs/web-crawler-plus) 

## Install

```bash

pip install invana-bot

```


## Working Examples

```python
# a simple usecase to use mongodb as cache and storage db.

from invana_bot import InvanaBot


if __name__ == '__main__':
    crawler = InvanaBot(
        database_credentials={
            "database": "crawler_test",
            "host": "127.0.0.1",
            "port": "27017",
        },
        database="mongodb",
    )
    crawler.run(urls=["https://medium.com/invanalabs", ],
                ignore_urls_with_words=['@'],
                allow_only_with_words=['/invanalabs'],
                )


```

```python
# a simple usecase to use solr as cache and storage db.

from invana_bot import InvanaBot

if __name__ == '__main__':
    # there is no database key for solr, it will be ignored
    crawler = InvanaBot(
        database_credentials={
            "host": "127.0.0.1",
            "port": "8983",
        },
        database="solr",
    )
    crawler.run(urls=["https://medium.com/invanalabs", ],
                ignore_urls_with_words=['@'],
                allow_only_with_words=['/invanalabs'],
                )


```

```python
# a simple usecase to use elasticsearch as cache and storage db.

from invana_bot import InvanaBot

if __name__ == '__main__':
    crawler = InvanaBot(
        database_credentials={
            "host": "127.0.0.1",
            "port": "9200",
        },
        database="elasticsearch",
    )
    crawler.run(urls=["https://medium.com/invanalabs", ],
                ignore_urls_with_words=['@'],
                allow_only_with_words=['/invanalabs'],
                )


```

## Extra settings 


- `WCP_SCRAPY_CRAWLER_TYPE` -  CrawlerRunner/CrawlerProcess

Checkout the lower level [documentation](docs/index.md) for more information.
