from invana_bot.parser import crawl_websites as _crawl_websites, crawl_feeds as _crawl_feeds
from invana_bot.settings import MONGODB_DEFAULTS, ELASTICSEARCH_DEFAULTS, \
    FEEDS_CRAWLER_DEFAULTS, WEBSITE_CRAWLER_DEFAULTS, SUPPORTED_DATABASES, SUPPORTED_CRAWLERS
from invana_bot.utils.config import validate_config, process_config
from scrapy.crawler import CrawlerProcess


class InvanaBot(object):
    """


    """
    settings = {
        'COMPRESSION_ENABLED': False,  # this will save the data in normal text form, otherwise to bytes form.
        'HTTPCACHE_ENABLED': True,
        'TELNETCONSOLE_PORT': None

    }
    process = None

    def __init__(self,
                 cache_database=None,
                 storage_database=None,
                 cache_database_uri=None,
                 storage_database_uri=None,
                 http_cache_enabled=True,
                 log_level="INFO",
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
        print("self.settings", self.settings)
        # self.is_settings_done = False

    def start_process(self):
        # self.is_settings_done = False
        self.process = CrawlerProcess(self.settings)

    def setup_database_settings(self, cache_database=None, storage_database=None,
                                ):

        if cache_database not in ["mongodb", "elasticsearch"]:
            raise Exception("we only support {} as cache_database".format(",".join(SUPPORTED_DATABASES)))

        if storage_database not in ["mongodb", "elasticsearch"]:
            raise Exception("we only support {} as storage_database ".format(",".join(SUPPORTED_DATABASES)))

        if cache_database == "mongodb":
            self.settings['HTTPCACHE_STORAGE'] = MONGODB_DEFAULTS['HTTPCACHE_STORAGE']
        if storage_database == "mongodb":
            self.settings['ITEM_PIPELINES'] = MONGODB_DEFAULTS['ITEM_PIPELINES']

        if cache_database == "elasticsearch":
            self.settings['HTTPCACHE_STORAGE'] = ELASTICSEARCH_DEFAULTS['HTTPCACHE_STORAGE']
        if storage_database == "elasticsearch":
            self.settings['ITEM_PIPELINES'] = ELASTICSEARCH_DEFAULTS['ITEM_PIPELINES']

    def setup_crawler_type_settings(self, crawler_type=None):
        if crawler_type == "websites":
            self.settings.update(WEBSITE_CRAWLER_DEFAULTS)
        elif crawler_type == "feeds":
            self.settings.update(FEEDS_CRAWLER_DEFAULTS)

        if self.cache_database_uri:
            self.settings['INVANA_BOT_SETTINGS']['HTTPCACHE_STORAGE_SETTINGS']['DATABASE_URI'] = self.cache_database_uri

        if self.storage_database_uri:
            self.settings['INVANA_BOT_SETTINGS']['ITEM_PIPELINES_SETTINGS']['DATABASE_URI'] = self.storage_database_uri

        # self.is_settings_done = True
        self.start_process()

    def _validate_urls(self, urls):
        if type(urls) is None:
            raise Exception("urls should be list type.")
        if len(urls) is 0:
            raise Exception("urls length should be atleast one.")

    def crawl_feeds(self, feed_urls=None):
        # if self.is_settings_done is False:
        self.setup_crawler_type_settings(crawler_type="feeds")
        self._validate_urls(feed_urls)
        _crawl_feeds(feed_urls=feed_urls, settings=self.settings)

    def start_jobs(self, jobs=None, stop_after_crawl=True):
        print("start_jobs", len(jobs))
        for job in jobs:
            print("**job", job[0], job[1])
            self.process.crawl(job[0], **job[1])
        self.process.start(stop_after_crawl=stop_after_crawl)

    def process_parser(self, parser_config=None):
        parser_config_cleaned = None
        if parser_config:
            is_valid_config = validate_config(config=parser_config)
            if is_valid_config:
                if parser_config.get("is_processed") == True:
                    parser_config_cleaned = parser_config
                    return parser_config_cleaned
                else:
                    parser_config_cleaned = process_config(parser_config)
                    parser_config_cleaned['is_processed'] = True
            else:
                raise Exception("invalid parser config")
        return parser_config_cleaned

    def crawl_websites(self,
                       urls=None,
                       ignore_urls_with_words=None,
                       allow_only_with_words=None,
                       follow=True,
                       parser_config=None,
                       context=None
                       ):
        # if self.is_settings_done is False:
        self.setup_crawler_type_settings(crawler_type="websites")

        self._validate_urls(urls)

        jobs = _crawl_websites(urls=urls,
                               ignore_urls_with_words=ignore_urls_with_words,
                               allow_only_with_words=allow_only_with_words,
                               follow=follow,
                               parser_config=parser_config,
                               context=context
                               )

        return jobs