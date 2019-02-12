from invana_bot import InvanaWebCrawler

extractor = {
    "extractor_name": "CustomContentExtractor",
    "data_selectors": [
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
    ],
}

detail_extractor = {
    "start_url": "https://blog.scrapinghub.com/the-crawlera-story",
    "data_selectors": [
        {
            "id": "blog_detail",
            "selector": ".blog-section",
            "selector_attribute": "element",
            "multiple": False
        },

        {
            "id": "title",
            "selector": "h1",
            "selector_type": "css",
            "selector_attribute": "text",
            "parent_selector": "blog_detail",
            "multiple": False
        },
        {
            "id": "published_at",
            "selector": ".date",
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
    ],

}

traversal = {
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
                extractor,  # invana is namespace or the developer username
                {"extractor_name": "ParagraphsExtractor", },  # invana is namespace or the developer username

            ],  # this will be converted into data_selectors when used by API.
            "traversals": [{
                "traversal_type": "pagination",
                "pagination": traversal,
                "next_pipe_id": "blog-list"
            }, {
                "traversal_type": "link_from_field",
                "link_from_field": {"extractor_name": "CustomContentExtractor", "field_name": "url"},
                "next_pipe_id": "blog-detail"
            }]
        },
        {  # single pipe
            "pipe_id": "blog-detail",
            "data_extractors": [
                detail_extractor,
            ]
        }
    ],
}
context = {

    "client_id": "abc",
    "job_id": "123"

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
