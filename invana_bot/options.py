from invana_bot.settings import MONGODB_DEFAULTS, ELASTICSEARCH_DEFAULTS, \
    FEEDS_CRAWLER_DEFAULTS, WEBSITE_CRAWLER_DEFAULTS, SUPPORTED_DATABASES, SUPPORTED_CRAWLERS
from invana_bot.pipelines.default import WebCrawlerPipeline, WebCrawlerPipelet
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.crawler import CrawlerProcess
from invana_bot.spiders.feeds import RSSSpider
from twisted.internet import reactor
import uuid
from datetime import datetime

from scrapy.utils.log import configure_logging


class InvanaCrawlerBase(object):
    """


    """
    settings = {
        'COMPRESSION_ENABLED': False,  # this will save the data in normal text form, otherwise to bytes form.
        'HTTPCACHE_ENABLED': True,
        'TELNETCONSOLE_PORT': None

    }
    runner = None
    jobs = []

    def __init__(self,
                 cache_database=None,
                 storage_database=None,
                 cache_database_uri=None,
                 storage_database_uri=None,
                 http_cache_enabled=True,
                 log_level="DEBUG",
                 extra_settings=None,
                 **kwargs):

        self.settings['HTTPCACHE_ENABLED'] = http_cache_enabled
        self.settings['LOG_LEVEL'] = log_level
        if extra_settings:
            self.settings.update(extra_settings)  # over riding or adding extra settings
        self.cache_database_uri = cache_database_uri
        self.storage_database_uri = storage_database_uri

        self.setup_database_settings(cache_database=cache_database,
                                     storage_database=storage_database
                                     )
        self.job_id = self.generate_job_id()
        self.set_logger()

    def set_logger(self):
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    def generate_job_id(self):
        return uuid.uuid4().hex

    def setup_database_settings(self, cache_database=None, storage_database=None,
                                ):

        if cache_database and cache_database not in ["mongodb", "elasticsearch"]:
            raise Exception("we only support {} as cache_database".format(",".join(SUPPORTED_DATABASES)))

        if storage_database and storage_database not in ["mongodb", "elasticsearch"]:
            raise Exception("we only support {} as storage_database ".format(",".join(SUPPORTED_DATABASES)))

        if cache_database == "mongodb":
            if self.settings['HTTPCACHE_ENABLED']:
                self.settings['HTTPCACHE_STORAGE'] = MONGODB_DEFAULTS['HTTPCACHE_STORAGE']
        if storage_database == "mongodb":
            self.settings['ITEM_PIPELINES'] = MONGODB_DEFAULTS['ITEM_PIPELINES']

        if cache_database == "elasticsearch":
            if self.settings['HTTPCACHE_ENABLED']:
                self.settings['HTTPCACHE_STORAGE'] = ELASTICSEARCH_DEFAULTS['HTTPCACHE_STORAGE']
        if storage_database == "elasticsearch":
            self.settings['ITEM_PIPELINES'] = ELASTICSEARCH_DEFAULTS['ITEM_PIPELINES']

    def setup_crawler_type_settings(self, crawler_type=None):
        if crawler_type == "websites":
            self.settings.update(WEBSITE_CRAWLER_DEFAULTS)
        elif crawler_type == "feeds":
            self.settings.update(FEEDS_CRAWLER_DEFAULTS)

        if self.settings['HTTPCACHE_ENABLED']:
            if self.cache_database_uri:
                self.settings['INVANA_BOT_SETTINGS']['HTTPCACHE_STORAGE_SETTINGS'][
                    'DATABASE_URI'] = self.cache_database_uri

        if self.storage_database_uri:
            self.settings['INVANA_BOT_SETTINGS']['ITEM_PIPELINES_SETTINGS']['DATABASE_URI'] = self.storage_database_uri

    def _validate_urls(self, urls):
        if type(urls) is None:
            raise Exception("urls should be list type.")
        if len(urls) is 0:
            raise Exception("urls length should be atleast one.")


class InvanaFeedCrawler(InvanaCrawlerBase):

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


class InvanaWebCrawler(InvanaCrawlerBase):
    """
    Split the bot into website crawler, feeds crawler, api crawler,

    """

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
        reactor.run()  # the script will block here until all crawling jobs are finished

    def set_pipeline(self, pipeline=None, context=None):
        self.setup_crawler_type_settings(crawler_type="websites")
        if context is None:
            context = {}
        context['job_id'] = self.job_id
        context['job_started'] = datetime.now()
        pipeline = WebCrawlerPipeline(pipeline=pipeline, job_id=self.job_id, context=context)
        jobs = pipeline.run()
        self.jobs.extend(jobs)
        return jobs

