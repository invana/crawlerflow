# web-scout

A micro-framework to crawl the web pages - blogs/rss. You can literally define what sites you 
want to crawl through and even configure the type of data you want to crawl and gather.

## Install

```bash

pip install git+https://github.com/invaana/web-crawler#egg=webcrawler

```

## Running and Usage 

```python


settings = {
    'FEED_URI': 'result.json',
    'ITEM_PIPELINES': {'__main__.MongoDBPipeline': 1} # custom Pipeline in the same file
}


``` 


