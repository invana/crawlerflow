# Single Crawlers

This is the simple form of crawling, this only requires crawling one website of a single structure.
Either crawling urls or traversing through pagination. But defined to only one website of single structure.



```bash
# path should have crawler_manifest.yml with the settings and crawler_transformations.py
# you need to create crawler_transformations.py even though you are not performing any transformation.

invana-bot --path . --type=single
```


## Single Crawler with traversal

In this example crawler `blog_list` is paginated for 4 times and extracted the data using 
the parsers `HTMLMetaTagExtractor`, `ParagraphExtractor`, `CustomContentExtractor`.

`extra_settings` tells few extra settings that will help the crawling run as expected without
any block from the site.

```yaml
# crawler_manifest.yml 
crawler_id: blog_list
start_urls:
- https://blog.scrapinghub.com
parsers:
- parser_type: HTMLMetaTagExtractor
  parser_id: meta_tags
- parser_type: ParagraphExtractor
  parser_id: paragraphs
- parser_type: CustomContentExtractor
  parser_id: blog_list_parser
  data_selectors:
  - selector_id: blogs
    selector: ".post-listing .post-item"
    selector_attribute: element
    multiple: true
    child_selectors:
    - selector_id: url
      selector: ".post-header h2 a"
      selector_type: css
      selector_attribute: href
      multiple: false
    - selector_id: title
      selector: ".post-header h2 a"
      selector_type: css
      selector_attribute: text
      multiple: false
    - selector_id: content
      selector: ".post-content"
      selector_type: css
      selector_attribute: html
      multiple: false
traversals:
- traversal_type: pagination
  pagination:
    selector: ".next-posts-link"
    selector_type: css
    max_pages: 2
  next_crawler_id: blog_list
settings:
  allowed_domains:
  - blog.scrapinghub.com
  download_delay: 2
context:
  author: https://github.com/rrmerugu
  description: Crawler that scrapes scrapinghub blogs


```


## Single crawler with traversal, transformation and indexing  

```yaml
# crawler_manifest.yml
crawler_id: blog_list
whitelisted_domains:
- blog.scrapinghub.com
start_urls:
- https://blog.scrapinghub.com
parsers:
- parser_type: HTMLMetaTagExtractor
  parser_id: meta_tags
- parser_type: ParagraphExtractor
  parser_id: paragraphs
- parser_type: CustomContentExtractor
  parser_id: blog_list_parser
  data_selectors:
  - selector_id: blogs
    selector: ".post-listing .post-item"
    selector_attribute: element
    multiple: true
    child_selectors:
    - selector_id: url
      selector: ".post-header h2 a"
      selector_type: css
      selector_attribute: href
      multiple: false
    - selector_id: title
      selector: ".post-header h2 a"
      selector_type: css
      selector_attribute: text
      multiple: false
    - selector_id: content
      selector: ".post-content"
      selector_type: css
      selector_attribute: html
      multiple: false
traversals:
- traversal_type: pagination
  pagination:
    selector: ".next-posts-link"
    selector_type: css
    max_pages: 2
  next_crawler_id: blog_list
transformations:
- transformation_id: default
  transformation_fn: transformation_fn
callbacks:
- callback_id: default
  index_id: default
  url: http://localhost/api/callback
  request_type: POST
  payload: {}
  headers:
    X-TOKEN: abc123456789
indexes:
- index_id: default
  transformation_id: default
  connection_uri: mongodb://127.0.0.1/crawlers_data_index
  collection_name: blog_list
  unique_key: url
settings:
  allowed_domains:
  - blog.scrapinghub.com
  download_delay: 5
context:
  author: https://github.com/rrmerugu
  description: Crawler that scrapes scrapinghub blogs

```