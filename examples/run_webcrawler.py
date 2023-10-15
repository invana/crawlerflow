import sys
sys.path.append("src")
from crawlerflow.runner import WebCrawler
from crawlerflow.utils import yaml_to_json

 
scraper_config_files = [
    "example-configs/webcrawler/APISpiders/api-publicapis-org.yml",
    "example-configs/webcrawler/HTMLSpiders/github-blog-list.yml",
    "example-configs/webcrawler/HTMLSpiders/github-blog-detail.yml"
]

crawlerflow = WebCrawler()

for scraper_config_file in scraper_config_files:
    scraper_config = yaml_to_json(open(scraper_config_file))
    crawlerflow.add_spider_with_config(scraper_config)
crawlerflow.start()