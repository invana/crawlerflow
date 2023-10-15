import sys
sys.path.append("src")
from web_scraper.runner import Crawlerflow
from web_scraper.utils import yaml_to_json


crawl_requests = yaml_to_json(open("example-configs/crawlerflow/requests/github-xml-urls.yml"))
spider_config = yaml_to_json(open("example-configs/crawlerflow/spiders/default-xml-spider.yml"))


flow = Crawlerflow()
flow.add_spider_with_config(crawl_requests, spider_config)
flow.start()