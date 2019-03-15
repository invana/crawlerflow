# InvanaBot Documentation


InvanaBot operates on **Crawl => Transform => Index** workflow. 


### About manifest.json:
- **cti_id** : unique identifier used to  
- **init_crawler** : json config that tells, from where the crawling should start.
    - **start_urls** 
- **crawlers** : a list of json based configurations that tells how to **traverse** and **parse** 
    - **parsers** : list of json configurations that tells crawler what data should be extracted from a web page.
    - **traversals** : list of json configurations that defines the pagination or which 
    page to goto.
- **transformations** : a list of python functions that can take `results` of current job as 
input and returns `cleaned_results` as output.
- **indexes** : a list of  that tells to what data storage, `cleaned_results` from different transformations 
 should be saved to 


Example of a full features manifest.json

```json

{
  "cti_id": "invanalab_xyz",
  "init_crawler": {
    "start_urls": [
      "https://blog.scrapinghub.com"
    ],
    "crawler_id": "blog-list"
  },
  "crawlers": [
    {
      "crawler_id": "blog-list",
      "parsers": [
        {
          "parser_type": "CustomContentExtractor",
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
                  "multiple": false
                },
                {
                  "id": "title",
                  "selector": ".post-header h2 a",
                  "selector_type": "css",
                  "selector_attribute": "text",
                  "multiple": false
                },
                {
                  "id": "content",
                  "selector": ".post-content",
                  "selector_type": "css",
                  "selector_attribute": "html",
                  "multiple": false
                }
              ]
            }
          ]
        }
      ],
      "traversals": [
        {
          "traversal_type": "pagination",
          "pagination": {
            "selector": ".next-posts-link",
            "selector_type": "css",
            "max_pages": 20
          },
          "next_crawler_id": "blog-list"
        },
        {
          "traversal_type": "link_from_field",
          "link_from_field": {
            "parser_type": "CustomContentExtractor",
            "parser_name": "url"
          },
          "next_crawler_id": "blog-detail"
        }
      ]
    }
  ],
  "transformations": [
  ],
  "indexes": [
    {
      "db_connection_uri": "mongodb://127.0.0.1/crawlers_data_index",
      "db_collection_name": "invanalabs_xyz"
    },
    {
      "db_connection_uri": "mongodb://127.0.0.1/crawlers_data_index",
      "db_collection_name": "invanalabs_xyz"
    }
  ],
  "callbacks": [
  ],
  "context": {
  }
}

```


### Traversals Types


```json

{
  "traversal_type": "pagination",
  "pagination": {
    "selector": ".next-posts-link",
    "selector_type": "css",
    "max_pages": 20
  },
  "next_crawler_id": "blog-list"
}


```
```json

{
  "traversal_type": "same_domain",
  "same_domain": {
    "max_pages": 1000
  },
  "next_crawler_id": "blog-list"
}
```

```json
{
  "traversal_type": "link_from_field",
  "link_from_field": {
    "parser_type": "CustomContentExtractor",
    "parser_name": "url"
  },
  "next_crawler_id": "blog-detail"
}
```

### Callback 

```json
{
  "callback_id": "default",
  "index_id": "default",
  "url": "http://localhost/api/callback",
  "request_type": "POST",
  "payload": {
  },
  "headers": {
    "X-TOKEN": "abc123456789"
  }
}
```