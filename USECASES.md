# InvanaBot UseCases

#### 1. UseCase I - Crawling a website

```python
# a simple usecase to use mongodb as cache and storage db.

from invana_bot import InvanaBot


if __name__ == '__main__':
    crawler = InvanaBot(
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

from invana_bot import InvanaBot
example_parser_config =  {
    "crawler_name": "scrapinghub-1",
    "domain": "scrapinghub.com",
    "subdomain": "blog.scrapinghub.com",
    "start_url": "https://blog.scrapinghub.com",
    "data_selectors": [
        {
            "id": "items",
            "selector": ".post-item",
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
        "selector_type": "css"
    }

}

crawler = InvanaBot(
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
from invana_bot import InvanaBot

if __name__ == '__main__':
    crawler = InvanaBot(
        cache_database_uri="127.0.0.1",
        storage_database_uri="127.0.0.1",
        cache_database="mongodb",
        storage_database="mongodb",
    )
    crawler.crawl_feeds(
        feed_urls=[
            # 'http://connect.iisc.ac.in/feed/',
            # "https://blog.google/rss/",
            # "https://blog.github.com/all.atom",
            # "https://githubengineering.com/atom.xml",
            # "http://blog.atom.io/feed.xml",
            # "https://phraseapp.com/blog/feed/",
            # "https://blog.bitbucket.org/feed/",
            # "https://scienceblog.com/feed/",
            "http://www.jimmunol.org/rss/current.xml",
            "http://feeds.nature.com/gt/rss/current",
            "http://feeds.nature.com/gene/rss/current",
            "http://feeds.nature.com/gim/rss/current",
            "http://feeds.nature.com/npjqi/rss/current",
            "http://feeds.nature.com/npjquantmats/rss/current",
            "http://feeds.nature.com/npjregenmed/rss/current"
        ]
    )


```



