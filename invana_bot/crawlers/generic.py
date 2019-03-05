from .base import InvanaCrawlerBase
from invana_bot.pipelines.default import CTIRunner
from datetime import datetime
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from twisted.internet import reactor


class InvanaWebCrawler(InvanaCrawlerBase):
    """
    Split the bot into website crawler, feeds crawler, api crawler,

    """

    def create_job(self, cti_config=None, context=None):
        self.setup_crawler_type_settings(crawler_type="websites")
        if context is None:
            context = {}
        if 'job_id' not in context.keys():
            context['job_id'] = self.job_id
            context['job_started'] = datetime.now()
        pipeline = CTIRunner(cti_config=cti_config, job_id=self.job_id, context=context)
        job = pipeline.run()
        return job

    def start_jobs(self, jobs=None):
        if self.runner is None:
            self.runner = CrawlerRunner(self.settings)
        for job in jobs:
            print (job)
            spider_cls = job['spider_cls']
            spider_kwargs = job['spider_kwargs']
            self.runner.crawl(spider_cls, **spider_kwargs)
        d = self.runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
