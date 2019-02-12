# InvanaCrawler UseCases

#### 1. UseCase I - Crawling a website

```python
# a simple usecase to use mongodb as cache and storage db.

from invana_bot.pipelines import InvanaCrawler



if __name__ == '__main__':
    crawler = InvanaCrawler(
        cache_database_uri="mongodb://127.0.0.1",
        storage_database_uri="127.0.0.1",
        cache_database="mongodb",
        storage_database="elasticsearch",
    )

    crawler.run(urls=["https://medium.com/invanalabs", ],
                ignore_urls_with_words=['@'],
                allow_only_with_words=['/invanalabs'],
                )


```


#### 1. UseCase II - Crawling with Pagination and extracting specific content(s)

```python

from invana_bot import InvanaCrawler


example_parser_config = {
    "crawler_name": "scrapinghub-1",
    "domain": "scrapinghub.com",
    "subdomain": "blog.scrapinghub.com",
    "start_url": "https://blog.scrapinghub.com",
    "data_selectors": [
        {
            "id": "items",
            "selector": ".post-listing .post-item",
            "selector_attribute": "element",
            "multiple": True
        },
        {
            "id": "url",
            "selector": ".post-header h2 a",
            "selector_type": "css",
            "selector_attribute": "href",
            "parent_selector": "items",
            "multiple": False
        },
        {
            "id": "title",
            "selector": ".post-header h2 a",
            "selector_type": "css",
            "selector_attribute": "text",
            "parent_selector": "items",
            "multiple": False
        },
        {
            "id": "content",
            "selector": ".post-content",
            "selector_type": "css",
            "selector_attribute": "html",
            "parent_selector": "items",
            "multiple": False
        }
    ],
    "next_page_selector": {
        "selector": ".next-posts-link",
        "selector_type": "css",
        "max_pages": 2
    }

}

crawler = InvanaCrawler(
    cache_database_uri="mongodb://127.0.0.1",
    storage_database_uri="127.0.0.1",
    cache_database="mongodb",
    storage_database="elasticsearch",
)
crawler.crawl_websites(urls=["https://blog.scrapinghub.com", ],
            parser_config=example_parser_config
            )




"""
crawler.crawl_websites(urls=["https://blog.scrapinghub.com", ],
            parser_config=example_parser_config,
            allow_only_with_words=['author'] # to follow only urls with the word author.
            )


""" 

            
```

####4. UseCase 2: Crawling the feeds

```python
from invana_bot import InvanaCrawler

if __name__ == '__main__':
    crawler = InvanaCrawler(
        cache_database_uri="127.0.0.1",
        storage_database_uri="127.0.0.1",
        cache_database="mongodb",
        storage_database="mongodb",
    )
    crawler.crawl_feeds(
        feed_urls=[
        "https://blog.scrapinghub.com/rss.xml"
        ]
    )


```


#### 5. Advanced example of settings.

```python



common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'LOG_LEVEL': 'INFO'
}

pipeline_settings = {
    'ITEM_PIPELINES': {'invana_bot.storages.elasticsearch.ElasticSearchPipeline': 1},
    'HTTPCACHE_STORAGE': "invana_bot.httpcache.elasticsearch.ESCacheStorage",
}

mongodb_settings = {
    'INVANA_BOT_SETTINGS': {
        'HTTPCACHE_STORAGE_SETTINGS': {
            'DATABASE_URI': "127.0.0.1",
            'DATABASE_NAME': "crawler_cache_db",
            'COLLECTION_NAME': "web_link",
            "EXPIRY_TIME": 3600
        },
        'ITEM_PIPELINES_SETTINGS': {
            'DATABASE_URI': "127.0.0.1",
            'DATABASE_NAME': "crawler_data",
            'COLLECTION_NAME': "crawler_feeds_data"
        }
    }
}

common_settings.update(pipeline_settings)
common_settings.update(mongodb_settings)



```


