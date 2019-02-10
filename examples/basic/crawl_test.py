from invana_bot import InvanaBot

client_info = {
    "domain": "scrapinghub.com",
    "subdomain": "blog.scrapinghub.com",
    "client_id": "invana",
    "crawler_pipeline_id": "11223",
    "crawler_name": "scrapinghub-1",

}

client_crawler_config = {
    "client_id": "tcl",
    "crawler_name": "bing_search_engine-1",
    "crawler_config": {
        "topics": [
            {
                "topic_name": "Jobs",
                "topic_keywords": ["jobs in food tech hyderabad", "jobs in food tech secunderabad "]
            },
            {
                "topic_name": "Agriculture",
                "topic_keywords": ["Agriculture advancements", "advancements in biotechnology"]
            },

        ]

    }
}


BING_CRAWLER_CONFIG = {
    "crawler_name": "search_engine_bing",
    "start_url": "https://www.bing.com/search",
    "data_selectors": [
        {
            "id": "items",
            "selector": ".b_algo",
            "selector_attribute": "element",
            "multiple": True
        },
        {
            "id": "url",
            "selector": "h2 a",
            "selector_type": "css",
            "selector_attribute": "href",
            "parent_selector": "items",
            "multiple": False
        },
        {
            "id": "title",
            "selector": "h2 a",
            "selector_type": "css",
            "selector_attribute": "text",
            "parent_selector": "items",
            "multiple": False
        },
        {
            "id": "description",
            "selector": ".b_caption p",
            "selector_type": "css",
            "selector_attribute": "text",
            "parent_selector": "items",
            "multiple": False
        }
    ],
    "next_page_selector": {
        "selector": "a.sb_pagN",
        "selector_type": "css",
        "max_pages": 2

    }

}


print("example_config", BING_CRAWLER_CONFIG)
if __name__ == '__main__':
    crawler = InvanaBot(
        cache_database_uri="mongodb://127.0.0.1",
        storage_database_uri="mongodb://127.0.0.1",
        cache_database="mongodb",
        storage_database="mongodb",
    )

    for topic in client_crawler_config['crawler_config']['topics']:
        for keyword in topic['topic_keywords']:
            context = {
                "client_id": "tcl",  # client id will be the namespace
                "topic_id": topic['topic_name'],
                "keyword": keyword
            }
            print("=****************************", keyword, topic['topic_name'])
            crawler.crawl_with_bing(keyword=keyword,
                                    context=context)
    crawler.start()