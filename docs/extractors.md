# Extractors 

InvanaBot allows users to extract information while it crawls through the webpages. You can specify multiple
extractors to a crawler, allowing you to organise the information you need into grouped/subdocument data.


All the extractors are available at `invana_bot.extractors`

## Standard Extractors

These are built-in extractors built with few usecases in mind.

1. ParagraphsExtractor
2. TableContentExtractor
3. HTMLMetaTagExtractor
4. CustomContentExtractor
5. ImageExtractor

### Usage

The extractors should be given to `parsers` list of a `crawler`. Each Parser should have a definition of 
`parser_type` and `parser_id`. During the crawl and extraction the extracted data will be saved to store as 
 `parser_id` (sub-document) in the overall data entry.

```yaml
crawlers:
- crawler_id: blog_list
  parsers:
  - parser_type: HTMLMetaTagExtractor
    parser_id: meta_tags
  - parser_type: ParagraphExtractor
    parser_id: paragraphs
```

## Custom Extractors 
This is non standard extractor which allows user to build their own extractor strategy.

1. CustomContentExtractor (non standard )

For custom extractor, You need to define what data to extract and how to save it in the db. You can either give just one or
multiple `selector` data or add child_selectors to any selector. 

**NOTE: Only one level of `child_selector` is only supported.**

## Usage


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