# Invana Bot

A batteries included crawler framework built on top of [scrapy](https://scrapy.org/)
 for generating crawling pipeline with json configs.


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
from invana_bot.schedulers.generic import InvanaJobScheduler
from invana_bot.pipelines.process import process_pipeline_config

list_extractor_selectors = [
    {
        "id": "blogs",
        "selector": ".post-listing .post-item",
        "selector_attribute": "element",
        "multiple": True
    },
    {
        "id": "url",
        "selector": ".post-header h2 a",
        "selector_type": "css",
        "selector_attribute": "href",
        "parent_selector": "blogs",
        "multiple": False
    },
    {
        "id": "title",
        "selector": ".post-header h2 a",
        "selector_type": "css",
        "selector_attribute": "text",
        "parent_selector": "blogs",
        "multiple": False
    },
    {
        "id": "content",
        "selector": ".post-content",
        "selector_type": "css",
        "selector_attribute": "html",
        "parent_selector": "blogs",
        "multiple": False
    }
]

detail_extractor_selectors = [
    {
        "id": "blog_detail",
        "selector": ".blog-section",
        "selector_attribute": "element",
        "multiple": False
    },

    {
        "id": "title",
        "selector": "h1 span",
        "selector_type": "css",
        "selector_attribute": "text",
        "parent_selector": "blog_detail",
        "multiple": False
    },
    {
        "id": "published_at",
        "selector": ".date a",
        "selector_type": "css",
        "selector_attribute": "text",
        "parent_selector": "blog_detail",
        "multiple": False
    }, {
        "id": "author",
        "selector": ".author a",
        "selector_type": "css",
        "selector_attribute": "text",
        "parent_selector": "blog_detail",
        "multiple": False
    },
    {
        "id": "html_content",
        "selector": ".post-body",
        "selector_type": "css",
        "selector_attribute": "html",
        "parent_selector": "blog_detail",
        "multiple": False
    }
]

traversal = {
    "selector": ".next-posts-link",
    "selector_type": "css",
    "max_pages": 2

}
pipeline_data = {
    "pipeline_id": "search_pipeline",
    "start_urls": ["https://blog.scrapinghub.com"],
    "pipeline": [
        {  # single pipe
            "pipe_id": "blog-list",
            "start_urls": ["https://blog.scrapinghub.com"],
            "data_extractors": [
                {
                    "extractor_name": "CustomContentExtractor",
                    "data_selectors": list_extractor_selectors
                },
                {
                    "extractor_name": "ParagraphsExtractor"
                },

            ],
            "traversals": [{
                "traversal_type": "pagination",
                "pagination": traversal,
                "next_parser_id": "blog-list"
            }, {
                "traversal_type": "link_from_field",
                "link_from_field": {"extractor_name": "CustomContentExtractor", "field_name": "url"},
                "next_parser_id": "blog-detail"
            }]
        },
        {
            "pipe_id": "blog-detail",
            "data_extractors": [
                {
                    "extractor_name": "CustomContentExtractor",
                    "data_selectors": detail_extractor_selectors
                },

            ]
        }
    ],
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

    pipeline_data = process_pipeline_config(pipeline=pipeline_data)

    all_job = crawler.create_job(
        pipeline=pipeline_data,
        context=context
    )

    scheduler = InvanaJobScheduler(settings=crawler.get_settings())
    scheduler.start_jobs(jobs=[all_job])


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


