# Traversals

There are two types of traversals available in the library now.

1. pagination
2. link_from_field




## pagination


```yaml


- traversal_type: pagination
pagination:
  selector: ".next-posts-link"
  selector_type: css
  max_pages: 1
next_crawler_id: blog_list
```

## link_from_field

This will traverse to the `url` field saved in `blog_list_parser` parser data.

```yaml
  - traversal_type: link_from_field
    link_from_field:
      parser_id: blog_list_parser
      selector_id: url
    next_crawler_id: blog_detail
```

Here is the example; the crawler will iterate through the `blogs` list data and follow the crawler with `url` field.
```json
 
 {
  "blog_list_parser": {
  "blogs": [
      {
          "url": "http://example/com/something",
          "title": "Some blog"
      }
    ]
  }
 }
```