from scrapy.linkextractors import LinkExtractor
from invana_bot.utils.crawlers import get_crawler_from_list
from invana_bot.runners.single import SingleCrawlerRunner
from invana_bot.utils.config import validate_cti_config
from transformers.transforms import OTManager
from transformers.executors import ReadFromMongo
from invana_bot.transformers.mongodb import WriteToMongoDB
from invana_bot.transformers.default import default_transformer
import requests
from .base import RunnerBase


class CTIFlowRunner(RunnerBase):
    """


    """

    def __init__(self, cti_manifest=None, settings=None, job_id=None, context=None, spider_cls=None):
        self.manifest = cti_manifest
        self.settings = settings
        self.crawlers = self.manifest['crawlers']
        self.job_id = job_id
        self.context = context
        self.spider_cls = spider_cls

    def crawl(self):
        errors = validate_cti_config(self.manifest)
        if len(errors) == 0:

            initial_crawler = get_crawler_from_list(
                crawler_id=self.manifest['init_crawler']['crawler_id'],
                crawlers=self.crawlers)
            initial_crawler['start_urls'] = self.manifest['init_crawler']['start_urls']
            crawler_runner = SingleCrawlerRunner(
                job_id=self.job_id,
                current_crawler=initial_crawler,
                crawlers=self.crawlers,
                context=self.context,
                spider_cls=self.spider_cls,
                settings=self.settings
            )
            cti_job = crawler_runner.run()

            return cti_job, errors
        else:
            return None, errors
