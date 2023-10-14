# WebScraper 

scrape data from web with no code (just YAML configs)

## Features

- [*] Extract structured data from HTML.  
- [*] Scrape API  
- [ ] Scrape XML feeds.
- [ ] Next traversal (Pagination)
- [ ] Custom Python Parser

## Concepts

### WebCrawler

```
from web_scraper import WebCrawler

# specify BOT_NAME, USER_AGENT, Downloader, 


```
 
### DataScraper

```

```

## Usage

### HTMLScraper

```python
html_text = """
<html>
    <body>
        <h1>Hello, Parsel!</h1>
        <ul class="header">
            <li><a href="http://example.com">Link 1</a></li>
            <li><a href="http://scrapy.org">Link 2</a></li>
        </ul>
        <main>Main text here</main>
    </body>
</html>
"""

```



## Usage 

```python
from WebScraper.runner import WebScraper
import yaml

scraper_config_file =   "example-configs/HTMLSpiders/github-blog-detail.yml"
web_scraper = WebScraper()

# custom_settings={
#     'BOT_NAME' = 'You bot Name' # if you dont specify, it will defaults to Scrapy bot name   
# }
# web_scraper = WebScraper(custom_settings=custom_settings)


scraper_config = yaml.safe_load(open(scraper_config_file))
web_scraper.add_spider_with_config(scraper_config)
web_scraper.start()
```
 