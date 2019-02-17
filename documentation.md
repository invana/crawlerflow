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
            "next_pipe_id": "blog-list"
        }, 
        {
            "traversal_type": "link_from_field",
            "link_from_field": {"extractor_name": "CustomContentExtractor", "field_name": "url"},
            "next_pipe_id": "blog-detail"
        }, 
        {
            "traversal_type": "same_domain",
            "next_pipe_id": "blog-list",
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
            "data_extractors": [   {
                    "extractor_name": "CustomContentExtractor",
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
                    "extractor_name": "ParagraphsExtractor"
                },

            ],
            "traversals": [{
                "traversal_type": "same_domain",
                "next_pipe_id": "blog-list"
            }]
        }
    ],
}
```