from invana_bot import InvanaBot

client_info = {
    "domain": "scrapinghub.com",
    "subdomain": "blog.scrapinghub.com",
    "client_id": "invana",
    "crawler_pipeline_id": "11223",
    "crawler_name": "scrapinghub-1",

}
example_config = {
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

print("example_config", example_config)
if __name__ == '__main__':
    crawler = InvanaBot(
        cache_database_uri="mongodb://127.0.0.1",
        storage_database_uri="mongodb://127.0.0.1",
        cache_database="mongodb",
        storage_database="mongodb",
        http_cache_enabled= False,
    )

    all_jobs = []

    for url in [
        "https://blog.scrapinghub.com",
        "https://blog.scrapinghub.com/page/3",
        "https://blog.scrapinghub.com/page/5"
    ]:
        parser_config = crawler.process_parser(parser_config=example_config)
        jobs = crawler.crawl_websites(
            urls=[
                url,
            ],
            parser_config=parser_config,
            context=client_info,
        )
        all_jobs.extend(jobs)
    crawler.start_jobs(jobs=all_jobs)
