import sys
sys.path.append("src")
from web_scraper.runner import Crawlerflow
from web_scraper.utils import yaml_to_json


requests_urls = yaml_to_json(open("example-configs/requests/github-detail-urls.yml"))
spider_config = yaml_to_json(open("example-configs/spiders/default-spider.yml"))

flow = Crawlerflow()
flow.add_spider_with_config(requests_urls, spider_config)
flow.start()