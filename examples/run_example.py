import sys
sys.path.append("src")
from web_scraper.runner import WebScraper
import yaml

 
scraper_config_files = [
    "example-configs/APISpiders/api-publicapis-org.yml",
    "example-configs/HTMLSpiders/github-blog-list.yml",
    "example-configs/HTMLSpiders/github-blog-detail.yml"
]

web_scraper = WebScraper()

for scraper_config_file in scraper_config_files:
    scraper_config = yaml.safe_load(open(scraper_config_file))
    web_scraper.add_spider_with_config(scraper_config)
web_scraper.start()