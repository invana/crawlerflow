# Invana Bot

A web crawler framework that can transform websites into datasets with Crawl, 
Transform and Index workflow. InvanaBot uses [MongoDB](https://www.mongodb.com/)
 as default database for caching and storage.


**NOTE: This project is under active development**

[![Build Status](https://travis-ci.org/invanalabs/invana-bot.svg?branch=master)](https://travis-ci.org/invanalabs/invana-bot) 
[![codecov](https://codecov.io/gh/invanalabs/invana-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/invanalabs/invana-bot) 


[**Features**](#features) | [**Install**](#install) | [**Usage**](#usage) | [**Support**](#support)


## Features

1. crawlers in the form of json configuration.

2. Define traversals from one parser to another.

3. Use standard extractors to scrape data like Tables, Paragraphs, Meta data of the page.

4. Define custom extractors to scrapy the data in the format you want - list of objects, list of strings, or dictionaries.

5. MongoDB as default Cache and Storage Database.

6. Headless web browsering - supports ajax and javascript based sites like 
single page applications(SPA) built on Angular, ReactJS or Veu

7. Transform and Index - You can add your transformation logic, that can format the crawled data and index 
into use specified storage. 



## Install

```bash
pip install git+https://github.com/invanalabs/invana-bot#egg=invana_bot
# This project is under constant development and might brake any previous implementation.
```



## Usage

```python


from invana_bot.crawlers.generic import InvanaBotWebCrawler
from invana_bot.settings import DEFAULT_SETTINGS


cti_config = {
  "cti_id": "invanalabs_xyz",
  "crawlers": {
    "start_urls": [
      "https://blog.scrapinghub.com"
    ],
    "crawlers": [
      {
        "crawler_id": "site_list",
        "parsers": [
          {
            "parser_name": "ParagraphsExtractor"
          }
        ],
        "traversals": [
          {
            "traversal_type": "same_domain",
            "next_crawler_id": "site_list"
          }
        ]
      }
    ]
  },
  "transformations": [
  ],
  "indexes": [
    {
      "db_connection_uri": "mongodb://127.0.0.1/crawlers_data_index",
      "db_collection_name": "invanalabs_xyz"
    }
  ],
  "callbacks": [
  ]
}
context = {
    "job_id": "123",
    "author": "https://github.com/rrmerugu",
    "description": "Crawler that scrapes invanalabs xyz"
}

if __name__ == '__main__':
    crawler = InvanaBotWebCrawler(
        settings=DEFAULT_SETTINGS
    )
    job = crawler.create_job(
        cti_config=cti_config,
        context=context
    )
    crawler.start_jobs(jobs=[job])


```


## Support

Feel free to [contact us](http://invanalabs.ai/contact-us/) for any further support.