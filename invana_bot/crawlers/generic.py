from .base import InvanaBotWebCrawlerBase
from invana_bot.pipelines.default import CTIRunner
from datetime import datetime
from twisted.internet import reactor
import copy
from scrapy import signals
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy.settings import Settings


class InvanaBotWebCrawler(InvanaBotWebCrawlerBase):
    """
    Invana bot web crawler

    """

    def create_job(self, cti_manifest=None, context=None):
        if context is None:
            context = {}
        if 'job_id' not in context.keys():
            context['job_id'] = self.job_id
            context['job_started'] = datetime.now()
        cti_runner = CTIRunner(cti_manifest=cti_manifest, settings=self.settings,
                               job_id=self.job_id, context=context)
        job, errors = cti_runner.crawl()
        return {"crawler_job": job, "crawler_job_errors": errors, "cti_runner": cti_runner}

    def start_job(self, job=None):
        runner = CrawlerRunner()
        crawler_job = job['crawler_job']
        cti_runner = job['cti_runner']
        spider_cls = crawler_job['spider_cls']
        spider_kwargs = crawler_job['spider_kwargs']

        def engine_stopped_callback():
            fn = copy.deepcopy(cti_runner.transform_and_index)
            fn()

        crawler = Crawler(spider_cls, Settings(cti_runner.settings))
        crawler.signals.connect(engine_stopped_callback, signals.engine_stopped)
        d = runner.crawl(crawler, **spider_kwargs)
        d.addBoth(engine_stopped_callback)
        reactor.run()
