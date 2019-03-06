# InvanaBot Documentation


InvanaBot operates on **Crawl => Transform => Index** workflow. 


###Terminology:

- **Parser config** : helps user to define the data that you want
 to extract and how you want to save it. 
 
 ```json

{
    "crawler_id": "blog-list",
    "parsers": [
      {
        "parser_name": "CustomContentExtractor",
        "data_selectors": [
          {
            "id": "blogs",
            "selector": ".post-listing .post-item",
            "selector_attribute": "element",
            "multiple": true,
            "child_selectors": [
              {
                "id": "url",
                "selector": ".post-header h2 a",
                "selector_type": "css",
                "selector_attribute": "href",
                "parent_selector": "blogs",
                "multiple": false
              },
              {
                "id": "title",
                "selector": ".post-header h2 a",
                "selector_type": "css",
                "selector_attribute": "text",
                "parent_selector": "blogs",
                "multiple": false
              },
              {
                "id": "content",
                "selector": ".post-content",
                "selector_type": "css",
                "selector_attribute": "html",
                "parent_selector": "blogs",
                "multiple": false
              }
            ]
          }
        ]
      }
    ],
    "traversals": [
      {
        "traversal_type": "same_domain",
        "next_crawler_id": "blog-list"
      }
    ]
}

```
 
- 