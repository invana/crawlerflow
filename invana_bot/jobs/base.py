import uuid
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from scrapy import signals
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy.settings import Settings


class CTIJobGeneratorBase(object):
    """


    """
    settings = {
        'COMPRESSION_ENABLED': False,  # this will save the data in normal text form, otherwise to bytes form.
        'HTTPCACHE_ENABLED': True,
        'TELNETCONSOLE_PORT': None

    }
    runner = None

    def __init__(self,
                 job_id=None,
                 settings=None,
                 **kwargs):

        if settings is None:
            raise Exception("settings should be set")
        self.settings = settings
        if job_id is None:
            self.job_id = self.generate_job_id()
        else:
            self.job_id = job_id
        self.set_logger()

    @staticmethod
    def set_logger():
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    @staticmethod
    def generate_job_id():
        return uuid.uuid4().hex

    def _validate_urls(self, urls):
        if type(urls) is None:
            raise Exception("urls should be list type.")
        if len(urls) is 0:
            raise Exception("urls length should be atleast one.")

    def get_settings(self):
        return self.settings

    def start_job(self, job=None, callback_fn=None):
        runner = CrawlerRunner()
        crawler_job = job['crawler_job']
        cti_runner = job['runner']
        crawler_cls = crawler_job['crawler_cls']
        crawler_kwargs = crawler_job['crawler_kwargs']

        def engine_stopped_callback():
            cti_runner.transform_and_index(callback_fn=callback_fn)

        if callback_fn:
            print("""
==========================================================
WARNING: callback_fn is {}
==========================================================
Since start_job is called with callback_fn, make sure you end the reactor if you want the crawler process to
stop after the callback function is executed. By default callback_fn=None will close the reactor.

To write a custom callback_fn

def callback_fn():
    print ("Write your own callback logic")
    from twisted.internet import reactor
    reactor.stop()
==========================================================
        """.format(callback_fn))

        crawler = Crawler(crawler_cls, Settings(cti_runner.settings))
        crawler.signals.connect(engine_stopped_callback, signals.engine_stopped)
        runner.crawl(crawler, **crawler_kwargs)
        """
        d = runner.crawl(crawler, **crawler_kwargs)
        # d.addBoth(engine_stopped_callback)
        """
        reactor.run()


"""
class InvanaFeedCrawler(CTIJobGeneratorBase):

    def crawl_feeds(self, feed_urls=None):
        self.setup_crawler_type_settings(crawler_type="feeds")
        self._validate_urls(feed_urls)

        process = CrawlerProcess(self.settings)
        allowed_domains = []
        for feed_url in feed_urls:
            domain = feed_url.split("://")[1].split("/")[0]  # TODO - clean this
            allowed_domains.append(domain)

        process.crawl(RSSSpider,
                      start_urls=feed_urls,
                      )
        process.start()

"""
