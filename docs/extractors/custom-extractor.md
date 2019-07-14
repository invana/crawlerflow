# Custom Extractor


Custom extractor allows user to build their own extractor data selectors.

## CustomContentExtractor


For custom extractor, You need to define what data to extract and how to save it in the db. You can either give just one or
multiple `selector` data or add child_selectors to any selector. 

**NOTE: Only one level of `child_selector` is only supported.**

### Usage


```yaml

crawlers:
- crawler_id: blog_list
  parsers:
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
```