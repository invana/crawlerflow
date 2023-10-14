from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .settings import DEFAULT_SETTINGS_OVERRIDES
from .utils import generate_uuid
import importlib
 

class WebScraper:

    """
    config_file =  "example-configs/HTMLSpiders/github-blog-detail.yml"
    web_scraper = WebScraper()

    scraper_config = yaml.safe_load(open(config_file))
     web_scraper.add_spider_with_config(scraper_config)
    web_scraper.start()
    """
    def __init__(self, settings_overrides=None, job_id=None) -> None:
        self.settings_overrides = settings_overrides or {}
        self.job_id = generate_uuid() if job_id is None else job_id
        self._process = None

    @property
    def settings(self):
        settings = dict(get_project_settings())
        for k, v in DEFAULT_SETTINGS_OVERRIDES.items():
            settings[k] = v
        for k, v in self.settings_overrides.items():
            settings[k] = v
        return settings

    @property
    def process(self):
        if self._process:
            return self._process
        self._process = CrawlerProcess(self.settings)
        return self._process

    def add_job_id(self, kwargs):
        kwargs['job_id'] = self.job_id
        return kwargs

    def add_spider(self, spider_cls, **kwargs):
        # https://doc.scrapy.org/en/latest/topics/spiders.html#spider-arguments
        self.process.crawl(spider_cls, **self.add_job_id(kwargs))
  
    def add_spider_with_config(self, spider_config):
        spider_cls = getattr(importlib.import_module(f"web_scraper.spiders"), spider_config['spider_type'])
        self.process.crawl(spider_cls, **self.add_job_id(spider_config))

    def start(self):
        self.process.start()  # the script will block here until all crawling jobs are finished


