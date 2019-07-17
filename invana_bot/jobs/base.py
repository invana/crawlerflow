import uuid
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from scrapy import signals
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy.settings import Settings
from invana_bot.utils.job import generate_job_id
from invana_bot.settings.default import DEFAULT_SETTINGS


class InvanaBotJobGeneratorBase(object):
    """


    """
    runner = CrawlerRunner()

    def __init__(self,
                 job_id=None,
                 settings=None,
                 **kwargs):

        if settings is None:
            raise Exception("settings should be set")
        self.settings = settings
        self.job_id = self.set_job_id(job_id=job_id)
        self.set_logger()

    @staticmethod
    def set_job_id(job_id=None):
        if job_id is None:
            job_id = generate_job_id()
        return job_id

    @staticmethod
    def set_logger():
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    @staticmethod
    def _validate_urls(urls):
        if type(urls) is None:
            raise Exception("urls should be list type.")
        if len(urls) is 0:
            raise Exception("urls length should be at least one.")

    def get_settings(self):
        return self.settings

    def start_job(self, job=None, callback_fn=None):
        print(job)
        spider_job = job['spider_job']
        runner = job['runner']
        spider_cls = spider_job['spider_cls']
        spider_settings = spider_job['spider_settings']
        spider_kwargs = spider_job['spider_kwargs']

        def engine_stopped_callback():
            runner.transform_and_index(callback_fn=callback_fn)

        if callback_fn:
            print("""
==========================================================
WARNING: callback_fn is {}
==========================================================
Since start_job is called with callback_fn, make sure you end the reactor if you want the spider process to
stop after the callback function is executed. By default callback_fn=None will close the reactor.

To write a custom callback_fn

def callback_fn():
    print ("Write your own callback logic")
    from twisted.internet import reactor
    reactor.stop()
==========================================================
        """.format(callback_fn))

        spider = Crawler(spider_cls, Settings(spider_settings))
        spider.signals.connect(engine_stopped_callback, signals.engine_stopped)
        self.runner.crawl(spider, **spider_kwargs)
        """
        d = runner.crawl(spider, **spider_kwargs)
        # d.addBoth(engine_stopped_callback)
        """
        reactor.run()
