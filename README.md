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



## Skills of the Bot

**1. Crawl a site and save the page content**: Use full for gathering the data and performing analytics on the page.

**2. Crawl a site and extract the content(s)**: This will extract the specific use full content(s) inside the pages(parsing the data). 

**3. Crawl and extract data from rss/atom feeds:** This will extract the data from the rss/atom feeds of the site you may want to follow.

**3. Analysers**: Built-in analysers to run on top the data like cleaning the data, categorize the data based on NLP, more on the roadmap.

**4. Seperate Cache and Storage Database Support**: There is difference in importance of the data for caching and storage, so
InvanaBot allows developer to implement seperate databases for caching and storage, where developer can use mongodb
for caching the crawled data, and storing the actual extracted data into elasticsearch, which can work as a instant search engine.


## Working Examples

```python
# a simple usecase to use mongodb as cache and storage db.

from invana_bot import InvanaBot


if __name__ == '__main__':
    crawler = InvanaBot(
        cache_database_uri="mongodb://127.0.0.1",
        storage_database_uri="mongodb://127.0.0.1",
        cache_database="mongodb",
        storage_database="elasticsearch",
    )
    """
    crawler = InvanaBot(
        cache_database_uri="127.0.0.1",
        storage_database_uri="127.0.0.1",
        cache_database="elasticsearch",
        storage_database="elasticsearch",
    )
    """
    crawler.run(urls=["https://medium.com/invanalabs", ],
                ignore_urls_with_words=['@'],
                allow_only_with_words=['/invanalabs'],
                )


```

 


## Extra settings 


- `WCP_SCRAPY_CRAWLER_TYPE` -  CrawlerRunner/CrawlerProcess

Checkout the lower level [documentation](docs/index.md) for more information.
