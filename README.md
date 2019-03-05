# Invana Bot

A web crawler framework that can transform websites into datasets with Crawl, Transform and Index Flow. 


It can use [MongoDB](https://www.mongodb.com/), [Elasticsearch](https://www.elastic.co/products/elasticsearch) 
and <del>[Solr](http://lucene.apache.org/solr/)</del> databases to cache the requests and 
also extract the data using parser configs 
and save them.


[![Build Status](https://travis-ci.org/invanalabs/invana-bot.svg?branch=master)](https://travis-ci.org/invanalabs/invana-bot) 
[![codecov](https://codecov.io/gh/invanalabs/invana-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/invanalabs/invana-bot) 

Look at the `examples/` folder for basic and advanced implementations.

## Install

```bash


pip install git+https://github.com/invanalabs/invana-bot#egg=invana_bot
# This project is under constant development and might brake any previous implementation.

```

## Usage

```python


from invana_bot.crawlers.generic import InvanaWebCrawler


cti_config = {
  "cti_id": "invanalabs-xyz",
  "crawlers": {
    "start_urls": [
      "https://blog.scrapinghub.com"
    ],
    "parsers": [
      {
        "parser_id": "site_list",
        "data_extractors": [
          {
            "extractor_name": "ParagraphsExtractor"
          }
        ],
        "traversals": [
          {
            "traversal_type": "same_domain",
            "next_parser_id": "site_list"
          }
        ]
      }
    ]
  },
  "transformations": [
  ],
  "indexes": [
    {
      "db_connection_uri": "mongodb://127.0.0.1"
    }
  ],
  "callbacks": [
  ]
}
context = {
    "job_start_time": "2019-1-1",
    "job_id": "123"
}

if __name__ == '__main__':
    crawler = InvanaWebCrawler(
        cache_database_uri="mongodb://127.0.0.1",
        storage_database_uri="mongodb://127.0.0.1",
        cache_database="mongodb",
        storage_database="mongodb",
    )


    job = crawler.create_job(
        cti_config=cti_config,
        context=context
    )
    crawler.start_jobs(jobs=[job])



```

## Skills of the Bot

**1. Crawl a site and save the page content**: Use full for gathering the data and performing analytics on the page.

**2. Crawl a site and extract the content(s)**: This will extract the specific use full content(s) inside the pages(parsing the data). 

**3. Crawl and extract data from rss/atom feeds:** This will extract the data from the rss/atom feeds of the site you may want to follow.

**4. Seperate Cache and Storage Database Support**: There is difference in importance of the data for caching and storage, so
InvanaCrawler allows developer to implement seperate databases for caching and storage, where developer can use mongodb
for caching the crawled data, and storing the actual extracted data into elasticsearch, which can work as a instant search engine.

**5. Transformers**: Built-in data transformers to run on top the data like cleaning the data, categorize the data based on NLP and more.

**6. Headless Browsers** [in roadmap]

**7. Taking screenshots while crawling** [in roadmap] for visual crawling



## License

MIT License


