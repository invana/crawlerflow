from .base import InvanaBotWebCrawlerBase
from invana_bot.pipelines.default import CTIRunner
from datetime import datetime
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


class InvanaBotWebCrawler(InvanaBotWebCrawlerBase):
    """
    Split the bot into website crawler, feeds crawler, api crawler,

    """

    def create_job(self, cti_config=None, context=None):
        if context is None:
            context = {}
        if 'job_id' not in context.keys():
            context['job_id'] = self.job_id
            context['job_started'] = datetime.now()
        cti_runner = CTIRunner(cti_config=cti_config, job_id=self.job_id, context=context)
        job = cti_runner.run()
        return job

    def start_jobs(self, jobs=None):
        if self.runner is None:
            self.runner = CrawlerRunner(self.settings)
        for job in jobs:
            print(job)
            spider_cls = job['spider_cls']
            spider_kwargs = job['spider_kwargs']
            self.runner.crawl(spider_cls, **spider_kwargs)
        d = self.runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
