# CrawlerFlow 

Web Crawlers orchestration framework that lets you create datasets from multiple web sources using yaml configurations.

## Features

Features
- [*] Write spiders in the YAML configs.
- [*] Create extractors to scrape data using YAML configs (HTML, API, RSS)
- [*] Define multiple extractors per spider.
- [*] Use standard extractors to scrape data like Tables, Paragraphs, Meta tags, JSON+LD of the page.
- [ ] Traverse between multiple websites.
- [ ] Write Python Extractors for advanced extraction strategy
<!-- - [ ] JMESPath integration for JSON trasnformations -->


 ## Installation

```
pip install git+https://github.com/invana/crawlerflow#egg=crawlerflow
```

## Usage

### Scraping with CrawlerFlow
```python
from web_scraper.runner import Crawlerflow
from web_scraper.utils import yaml_to_json


crawl_requests = yaml_to_json(open("example-configs/crawlerflow/requests/github-detail-urls.yml"))
spider_config = yaml_to_json(open("example-configs/crawlerflow/spiders/default-spider.yml"))
github_default_extractor = yaml_to_json(open("example-configs/crawlerflow/extractors/github-blog-detail.yml"))

flow = Crawlerflow()
flow.add_spider_with_config(crawl_requests, spider_config, default_extractor=github_default_extractor)
flow.start()
```

### Scraping with WebCrawler

```python
from web_scraper.runner import WebCrawler
from web_scraper.utils import yaml_to_json

 
scraper_config_files = [
    "example-configs/webcrawler/APISpiders/api-publicapis-org.yml",
    "example-configs/webcrawler/HTMLSpiders/github-blog-list.yml",
    "example-configs/webcrawler/HTMLSpiders/github-blog-detail.yml"
]

web_scraper = WebCrawler()

for scraper_config_file in scraper_config_files:
    scraper_config = yaml_to_json(open(scraper_config_file))
    web_scraper.add_spider_with_config(scraper_config)
web_scraper.start()
```

Refer `examples-configs/` folder for example configs.


## Available Extractors

- [*] HTMLExtractor
- [*] MetaTagExtractor
- [*] JSONLDExtractor
- [*] TableContentExtractor
- [*] IconsExtractor
 
 