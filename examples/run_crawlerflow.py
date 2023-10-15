import sys
sys.path.append("src")
from crawlerflow.runner import Crawlerflow
from crawlerflow.utils import yaml_to_json


crawl_requests = yaml_to_json(open("example-configs/crawlerflow/requests/github-detail-urls.yml"))
spider_config = yaml_to_json(open("example-configs/crawlerflow/spiders/default-spider.yml"))
github_default_extractor = yaml_to_json(open("example-configs/crawlerflow/extractors/github-blog-detail.yml"))

flow = Crawlerflow()
flow.add_spider_with_config(crawl_requests, spider_config, default_extractor=github_default_extractor)
flow.start()