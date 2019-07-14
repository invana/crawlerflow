# Manifest


InvanaBot crawls, transforms and indexes the data from multiple web sources. 


## Spiders

InvanaBot supports 3 types of spiders - 1. web 2. Feeds 3. API. There is no difference in the manifest for web,
feeds or API. The difference exists only in the way you execute `invana-bot` command.


```yaml
- spider_id: default_spider
  allowed_domains:
    - blog.scrapinghub.com
  headers:
    - key : value
  settings:
    - key : value
```

## Extractors 

```yaml
- spider_id: default_spider
  extractors:
  - extractor_type: PageOverviewExtractor
    extractor_id: overview
```


## Traversals 

This will help the spiders traverse from one domain to the other or with-in the domain.

```yaml
- spider_id: default_spider
  extractors:
  - extractor_type: PageOverviewExtractor
    extractor_id: overview
  traversals:
  - traversal_id: bing_pagination
    selector_value: a.sb_pagN
    selector_type: css
    max_pages: 5
    next_spider_id: bing_search
```

## Transformations

This is the transformation that can be applied on all the data crawled from a single run. This will 
be executed after the whole job is done.


- **transformation_id** - name of the transformation
- **transformation_fn** - string of python code with a function with the name of 
transformation_id.

Here is the transformation config:

```yaml
- spider_id: default_spider
  extractors:
  - extractor_type: PageOverviewExtractor
    extractor_id: overview
  transformations:
  - transformation_id: default_transformation
    transformation_fn : """
#!/usr/bin/env python

def default_transformation(data):
  # TODO modify the data according to your needs.
  return data
"""
```

## Indexes

This is where the data extracted during the spiders will be saved. Currently InvanaBot 
supports [MongoDB](https://www.mongodb.com/) and [Elasticsearch](https://www.elastic.co/products/elasticsearch).




### Example usage

```yaml
- spider_id: default_spider
  allowed_domains:
    - blog.scrapinghub.com
  extractors:
  - extractor_type: PageOverviewExtractor
    extractor_id: overview
  transformations:
  - transformation_id: default_transformation
    transformation_fn : """
#!/usr/bin/env python

def default_transformation(data):
  # TODO modify the data according to your needs.
  return data
"""  
  indexes:
  - index_id: default_index
  transformation_id: default_transformation
  connection_uri: mongodb://127.0.0.1/spiders_data_index
  collection_name: default_spider
  unique_key: url

```
