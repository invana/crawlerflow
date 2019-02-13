from invana_bot import InvanaWebCrawler

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

pagination_traversal = {
    "selector": ".next-posts-link",
    "selector_type": "css",
    "max_pages": 2

}
pipeline_data = {
    "pipeline_id": "search_pipeline",
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
                "pagination": pagination_traversal,
                "next_pipe_id": "blog-list"
            }, {
                "traversal_type": "link_from_field",
                "link_from_field": {"extractor_name": "CustomContentExtractor", "field_name": "url"},
                "next_pipe_id": "blog-detail"
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
    "extra_info": "2019-1-1 something",
    "author": "Ravi@Invana",

}

if __name__ == '__main__':
    crawler = InvanaWebCrawler(
        cache_database_uri="mongodb://127.0.0.1",
        storage_database_uri="mongodb://127.0.0.1",
        cache_database="mongodb",
        storage_database="mongodb",
    )

    all_jobs = crawler.set_pipeline(
        pipeline=pipeline_data,
        context=context
    )
    crawler.start_jobs(jobs=all_jobs)
