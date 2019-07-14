# Invana Bot Documentation



### Traversal Types
```python

{ 
"pagination": [
        {
            "traversal_type": "pagination",
            "pagination": {
                "selector": ".next-posts-link",
                "selector_type": "css",
                "max_pages": 2
                },
            "next_spider_id": "blog-list"
        }, 
        {
            "traversal_type": "link_from_field",
            "link_from_field": {"extractor_type": "CustomContentExtractor", "extractor_id": "url"},
            "next_spider_id": "blog-detail"
        }, 
        {
            "traversal_type": "same_domain",
            "next_spider_id": "blog-list",
            "max_pages": 2
        },
            
            
    ]}

```


### Data Extractors

```python

pipeline_data = {
    "pipeline_id": "generic_crawling_pipeline",
    "start_urls": ["https://selenium-python.readthedocs.io"],
    "pipeline": [
        {  # single pipe
            "pipe_id": "blog-list",
            "extractors": [   {
                    "extractor_type": "CustomContentExtractor",
                    "data_selectors": [
                        {
                            "id": "main_content_html",
                            "selector": ".body",
                            "selector_type": "css",
                            "selector_attribute": "html",
                            "multiple": False
                        }
                    ]
                },
                {
                    "extractor_type": "ParagraphsExtractor"
                },

            ],
            "traversals": [{
                "traversal_type": "same_domain",
                "next_spider_id": "blog-list"
            }]
        }
    ],
}
```