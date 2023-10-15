# CrawlerFlow 

scrape data from web with no code (just YAML configs)

## Features

- [*] Extract structured data from HTML.  
- [*] Scrape API  
- [ ] Scrape XML feeds.
- [ ] Next traversal (Pagination)
- [ ] Custom Python Parser
- [ ] JMESPath Parser for extractors

 
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
 
 