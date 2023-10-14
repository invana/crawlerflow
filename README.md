# WebScraper 

scrape data from web with no code (just YAML configs)

## Features

- [*] Extract structured data from HTML.  
- [*] Scrape API  
- [ ] Scrape XML feeds.
- [ ] Next traversal (Pagination)
- [ ] Custom Python Parser


## Usage 

```python
from WebScraper.runner import WebScraper
import yaml

scraper_config_file =   "example-configs/HTMLSpiders/github-blog-detail.yml"



web_scraper = WebScraper()

# settings_overrides={
#     'BOT_NAME' = 'You bot Name' # if you dont specify, it will defaults to Scrapy bot name   
# }
# web_scraper = WebScraper(settings_overrides=settings_overrides)


scraper_config = yaml.safe_load(open(scraper_config_file))
web_scraper.add_spider_with_config(scraper_config)
web_scraper.start()
```
 