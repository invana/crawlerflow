from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


class InvanaJobScheduler(object):
    """
    This will actually schedule the jobs.

    crawler = InvanaBotWebCrawler(
        cache_database_uri="mongodb://127.0.0.1",
        storage_database_uri="mongodb://127.0.0.1",
        cache_database="mongodb",
        storage_database="mongodb",
    )

    all_jobs = crawler.create_job(
        pipeline=pipeline_data,
        context=context
    )

    scheduler = InvanaJobScheduler(settings=crawler.get_settings(), jobs=crawler.get_jobs())
    scheduler.start()



    """
    jobs = []
    runner = None

    def __init__(self, settings=None):
        self.settings = settings

    def start(self):
        self.start_jobs(jobs=self.jobs)

    def start_jobs(self, jobs=None):
        if self.runner is None:
            self.runner = CrawlerRunner(self.settings)
        for job in jobs:
            spider_cls = job['spider_cls']
            spider_kwargs = job['spider_kwargs']
            self.runner.crawl(spider_cls, **spider_kwargs)
        d = self.runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
