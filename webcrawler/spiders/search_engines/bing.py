from webcrawler.spiders.search_engines.base import SearchEngineBaseSpider
from scrapy.crawler import CrawlerProcess
from webcrawler.utils.config import validate_config, process_config

BING_SELECTOR_CONFIG = {
    "crawler_name": "search_engine_bing",
    "start_url": "https://www.bing.com/search",
    "data_selectors": [
        {
            "id": "items",
            "selector": "#b_results h2",
            "selector_attribute": "element",
            "multiple": True
        },
        {
            "id": "url",
            "selector": "a",
            "selector_type": "css",
            "selector_attribute": "href",
            "parent_selector": "items",
            "multiple": False
        },
        {
            "id": "title",
            "selector": "a",
            "selector_type": "css",
            "selector_attribute": "text",
            "parent_selector": "items",
            "multiple": False
        }
    ],
    "next_page_selector": {
        "selector": "a.sb_pagN",
        "selector_type": "css"
    }

}


def crawl_with_bing(settings=None, topic=None):
    config = BING_SELECTOR_CONFIG
    validate_config(config=config)
    config = process_config(config)
    process = CrawlerProcess(settings)
    start_url = "{}?q={}".format(config.get('start_url'), topic)

    process.crawl(SearchEngineBaseSpider,
                  start_urls=[start_url],
                  name=config.get('crawler_name'),
                  config=config
                  )
    process.start()
