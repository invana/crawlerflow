from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


class InvanaJobScheduler(object):
    """
    This will actually schedule the jobs.

    crawler = InvanaWebCrawler(
        cache_database_uri="mongodb://127.0.0.1",
        storage_database_uri="mongodb://127.0.0.1",
        cache_database="mongodb",
        storage_database="mongodb",
    )

    all_jobs = crawler.create_jobs(
        pipeline=pipeline_data,
        context=context
    )

    scheduler = InvanaJobScheduler(settings=crawler.get_settings(), jobs=crawler.get_jobs())
    scheduler.start()



    """
    jobs = []
    runner = None

    def __init__(self, settings=None, jobs=None):
        self.settings = settings
        self.jobs = jobs if jobs else []

    def start(self):
        self.start_jobs(jobs=self.jobs)

    def start_jobs(self, jobs=None):
        if self.runner is None:
            self.runner = CrawlerRunner(self.settings)
        for job in jobs:
            spider_cls = job[0]
            spider_kwargs = job[1]
            self.runner.crawl(spider_cls, **spider_kwargs)
        d = self.runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
