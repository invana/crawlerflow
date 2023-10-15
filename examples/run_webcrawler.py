import sys
sys.path.append("src")
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