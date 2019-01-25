# Invana Bot

A batteries included crawler framework built on top of [scrapy](https://scrapy.org/) for scale and intelligent crawling.

It can use [MongoDB](https://www.mongodb.com/), [Elasticsearch](https://www.elastic.co/products/elasticsearch) 
and <del>[Solr](http://lucene.apache.org/solr/)</del> databases to cache the requests and also extract the data using parser configs 
and save them.


[![Build Status](https://travis-ci.org/invanalabs/web-crawler-plus.svg?branch=master)](https://travis-ci.org/invanalabs/web-crawler-plus) 
[![codecov](https://codecov.io/gh/invanalabs/web-crawler-plus/branch/master/graph/badge.svg)](https://codecov.io/gh/invanalabs/web-crawler-plus) 

Look at the `examples/` folder for basic and advanced implementations.

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

**5. ProxyRotator** [in roadmap]

**6. Headless Browsers** [in roadmap]

**7. Taking screenshots while crawling** [in roadmap] for visual crawling


