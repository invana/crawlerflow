# Quickstart

We're going to create a simple single domain crawler to get the extract the blogs and save to MongoDB and 
Elasticsearch.

## 1. Installation

```bash

# Create the project directory
mkdir tutorial 
cd tutorial


# Create a virtual environment to isolate our package dependencies locally
python3 -m venv venv
source venv/bin/activate  # On Windows use `env\Scripts\activate`

# Install InvanaBot into the virtual environment
pip3 install invana-bot


```

## 2. Create Spider
```bash
# Setup a new spider
cat > cti_manifest.yml <<EOF
cti_id: scrapinghub_blogs
init_crawler:
  start_urls:
  - "https://blog.scrapinghub.com"
  spider_id: blog_list
spiders:
- spider_id: blog_list
  allowed_domains:
    - "blog.scrapinghub.com"
  traversals:
  - traversal_id: scrapinghub_pagination
    selector_type: css
    selector_value: ".next-posts-link"
    max_pages: 1
    next_spider_id: blog_list
  - traversal_id: scrapinghub_detail
    selector_type: css
    selector_value: "h2 a"
    max_pages: 1
    next_spider_id: blog_detail
- spider_id: blog_detail
  extractors:
  - extractor_type: CustomContentExtractor
    extractor_id: blog_detail
    data_selectors:
    - selector_id: blog_detail
      selector: ".blog-section"
      selector_attribute: element
      data_type: DictField
      child_selectors:
      - selector_id: title
        selector: h1 span
        selector_type: css
        selector_attribute: text
        data_type: StringField
      - selector_id: published_at
        selector: ".date a"
        selector_type: css
        selector_attribute: text
        data_type: StringField
      - selector_id: author
        selector: ".author a"
        selector_type: css
        selector_attribute: text
        data_type: StringField
data_storages:
- data_storage_id: default
  transformation_id: default
  connection_uri: mongodb://127.0.0.1/spiders_data_index
  collection_name: scrapinghub_blogs
  unique_key: url
settings:
  allowed_domains:
  - "blog.scrapinghub.com"
  download_delay: 0
context:
  author: https://github.com/rrmerugu
  description: Crawler that scrapes scrapinghub blogs
EOF
```


## 3. Run the Spider


```bash
invana-bot --type=web
```