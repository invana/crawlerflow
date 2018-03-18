"""
Look at https://doc.scrapy.org/en/latest/topics/practices.html for usage

"""
import scrapy
from scrapy.crawler import CrawlerProcess
from webcrawler.spiders.website import InvanaWebsiteSpider
from webcrawler.spiders.generic import InvaanaGenericSpider
from webcrawler.spiders.feeds import GenericFeedSpider, RSSSpider
from scrapy.linkextractors import LinkExtractor
from webcrawler.utils.config import validate_config, process_config
from scrapy.spiders import Rule
import re


def crawler(config=None,
            settings=None):
    print(settings)
    if settings is None:
        settings = {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        }
    if "USER_AGENT" not in settings.keys():
        settings['USER_AGENT'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'  # TODO - make this random
    validate_config(config=config)
    config = process_config(config)
    process = CrawlerProcess(settings)

    process.crawl(InvaanaGenericSpider,
                  start_urls=[config.get('start_url')],
                  name=config.get('crawler_name'),
                  config=config
                  )
    process.start()


def crawle_multiple_websites(urls=None,
                             settings=None,
                             ignore_urls_with_words=None,
                             follow=True):
    # TODO - usage of stop_after_crawl=False will leave the process at the end, need to fix this
    for url in urls:
        crawl_website(url=url, settings=settings, ignore_urls_with_words=ignore_urls_with_words,
                      follow=follow,
                      stop_after_crawl=False)


def crawl_website(url=None, settings=None,
                  ignore_urls_with_words=None,
                  allow_only_with_words=None, follow=True,
                  stop_after_crawl=True):
    if ignore_urls_with_words is None:
        ignore_urls_with_words = []

    if allow_only_with_words is None:
        allow_only_with_words = []

    extractor_options = {}
    if len(ignore_urls_with_words) > 0:
        ignored_words_regex = [re.compile(word) for word in ignore_urls_with_words]
        extractor_options['deny'] = ignored_words_regex

    if len(allow_only_with_words) > 0:
        allow_only_words_regex = [re.compile(word) for word in allow_only_with_words]
        extractor_options['allow'] = allow_only_words_regex

    extractor = LinkExtractor(**extractor_options)

    rules = [
        Rule(extractor, callback='parse_item', follow=follow)
    ]
    process = CrawlerProcess(settings)
    domain = url.split("://")[1].split("/")[0]  # TODO - clean this
    process.crawl(InvanaWebsiteSpider, start_urls=[url],
                  allowed_domains=[domain],
                  rules=rules
                  )
    process.start(stop_after_crawl=stop_after_crawl)


def crawl_with_search_engine():
    pass


def crawl_feeds(feed_urls=None, settings=None):
    if settings is None:
        settings = {}
    process = CrawlerProcess(settings)
    allowed_domains = []
    for feed_url in feed_urls:
        domain = feed_url.split("://")[1].split("/")[0]  # TODO - clean this
        allowed_domains.append(domain)

    # print(allowed_domains)
    process.crawl(RSSSpider,
                  start_urls=feed_urls,
                  )
    process.start()
