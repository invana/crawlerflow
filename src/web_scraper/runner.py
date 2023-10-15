from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .settings import DEFAULT_SETTINGS_OVERRIDES
from .exceptions import DefaultExtractorRequired
from .utils import generate_uuid
from slugify import slugify
from .request import CrawlRequest
import importlib
import scrapy


class WebScraperBase:


    def __init__(self,  custom_settings=None, job_id=None) -> None:
        self.custom_settings = custom_settings or {}
        self.job_id = generate_uuid() if job_id is None else job_id
        self._process = None

    @property
    def settings(self):
        settings = dict(get_project_settings())
        for k, v in DEFAULT_SETTINGS_OVERRIDES.items():
            settings[k] = v
        for k, v in self.custom_settings.items():
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

    def _start(self):
        self.process.start()  # the script will block here until all crawling jobs are finished

    def start(self):
        self._start()


class WebCrawler(WebScraperBase):

    """
    config_file =  "example-configs/HTMLSpiders/github-blog-detail.yml"
    web_scraper = WebCrawler()

    scraper_config = yaml.safe_load(open(config_file))
     web_scraper.add_spider_with_config(scraper_config)
    web_scraper.start()
    """

    def add_spider_with_config(self, spider_config):
        spider_cls = getattr(importlib.import_module(
            f"web_scraper.spiders"), spider_config['spider_type'])
        self.process.crawl(spider_cls, **self.add_job_id(spider_config))


class Crawlerflow(WebScraperBase):
    """
    flow = Crawlerflow()

    
    """

    def add_spider_with_config(self, crawl_requests,  spider_config, default_extractor=None):

        spider_config['name'] = slugify(spider_config['name'])
        if spider_config['spider_type'] == "HTMLSpider":
            if default_extractor is None:
                raise DefaultExtractorRequired()
            spider_config['default_extractor'] = default_extractor
        crawl_requests = [CrawlRequest(**req) for req in crawl_requests]

        spider_config['crawl_requests'] = crawl_requests
        spider_cls = getattr(importlib.import_module(
            f"web_scraper.spiders"), spider_config['spider_type'])
        self.add_spider(spider_cls, **self.add_job_id(spider_config) )