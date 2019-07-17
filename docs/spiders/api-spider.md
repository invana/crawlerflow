# API Spider

Create a manifest.yml and run the spider.


```yaml
cti_id: localhost-auditlogs
init_spider:
  spider_id: default
  start_urls:
    - http://localhost:8000/api/index/spider/data?page=1&crawled_id=bing_search&extractor_id=bing-search-result&job_id=5d25d414b7ba3e4972172913&token=b1d0801131a542d98a492916da362612
spiders:
- spider_id: default
  allowed_domains:
  - localhost:8000
  extra_url_param: crawled_id=bing_search&extractor_id=bing-search-result&job_id=5d25d414b7ba3e4972172913&token=b1d0801131a542d98a492916da362612
  pagination_param: page
  result_key: result
settings:
  allowed_domains:
  - "localhost:8000"
  download_delay: 0
context:
  author: https://github.com/rrmerugu
  description: Crawler that scrapes audit logs


```



## Running the Spider

```bash
invana-bot --type=api
```