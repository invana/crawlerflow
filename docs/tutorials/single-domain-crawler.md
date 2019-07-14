# Single Domain Crawler



This is the simple form of crawling, this only requires crawling one website of a single structure.
Either crawling urls or traversing through pagination. But defined to only one website of single structure.



```bash
# path should have crawler_manifest.yml with the settings and crawler_transformations.py
# you need to create crawler_transformations.py even though you are not performing any transformation.
# refer examples/run-single-crawler/ folder for reference files that should exist in path.

invana-bot --path . --type=single
```

## Single Crawler with traversal

In this example crawler `blog_list` is paginated for 2 times and extracted the data using 
the extractors `MetaTagExtractor`, `ParagraphExtractor`, `CustomContentExtractor`.

`extra_settings` tells few extra settings that will help the crawling run as expected without
any block from the site.

```yaml
# crawler_manifest.yml 
spider_id: blog_list
start_urls:
- https://blog.scrapinghub.com
extractors:
- extractor_type: MetaTagExtractor
  extractor_id: meta_tags
- extractor_type: ParagraphExtractor
  extractor_id: paragraphs
- extractor_type: CustomContentExtractor
  extractor_id: blog_list_parser
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
  next_spider_id: blog_list
settings:
  allowed_domains:
  - blog.scrapinghub.com
  download_delay: 5
context:
  author: https://github.com/rrmerugu
  description: Crawler that scrapes scrapinghub blogs


```

