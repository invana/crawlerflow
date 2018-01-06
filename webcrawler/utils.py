example_config = {
    "crawler_name": "scrapinghub-1",
    "domain": "scrapinghub.com",
    "subdomain": "blog.scrapinghub.com",
    "start_url": "https://blog.scrapinghub.com",
    "start_urls": [],  # use either start_url or start_urls
    "data_selectors": [
        {
            "id": "blog",
            "selector": "post-content",
            "selector_attribute": "element",
            "multiple": True
        },
        {
            "id": "site_title",
            "selector": ".site-title",
            "selector_type": "css",
            "selector_attribute": "text",
            "multiple": False
        },
        {
            "id": "title",
            "selector": "h2.entry-title",
            "selector_type": "css",
            "selector_attribute": "text",
            "parent_selector": "blog",
            "multiple": False
        },
        {
            "id": "content",
            "selector": ".entry-summary",
            "selector_type": "css",
            "selector_attribute": "html",
            "parent_selector": "blog",
            "multiple": False
        }
    ],
    "next_page_selector": {
        "selector": "div.prev-post > a",
        "selector_type": "css",
    }

}
