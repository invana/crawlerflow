# InvanaBot UseCases



#### 1. UseCase I - Crawling with Pagination and extracting specific content(s)

```python
# example_parser_with_pagination.py

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


