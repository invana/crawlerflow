"""
Look at https://doc.scrapy.org/en/latest/topics/practices.html for usage

"""
from scrapy.crawler import CrawlerProcess
from invana_bot.spiders.websites import InvanaWebsiteSpider, InvanaWebsiteParserSpider
from invana_bot.spiders.feeds import RSSSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import re


def crawl_websites(urls=None,
                   ignore_urls_with_words=None,
                   allow_only_with_words=None,
                   parser_config=None,
                   context=None,
                   follow=True,
                   ):
    """
    crawl multiple sites

    :param urls:
    :param ignore_urls_with_words:
    :param follow:
    :param parser_config:
    :return:
    """
    jobs = []
    for url in urls:
        spider_cls, spider_kwargs = crawl_website(url=url,
                                                  ignore_urls_with_words=ignore_urls_with_words,
                                                  allow_only_with_words=allow_only_with_words,
                                                  parser_config=parser_config,
                                                  context=context,
                                                  follow=follow)

        jobs.append([spider_cls, spider_kwargs])
        # process.crawl(spider_cls,
        #               **spider_kwargs
        #               ) # sending crawl jobs into a process.
    return jobs


def crawl_website(url=None,
                  ignore_urls_with_words=None,
                  allow_only_with_words=None,
                  parser_config=None,
                  follow=True,
                  context=None):
    """
    Crawl a single site

    :param url:
    :param ignore_urls_with_words:
    :param allow_only_with_words:
    :param follow:
    :param parser_config:
    :param context:
    :return:
    """

    ignore_urls_with_words = [] if ignore_urls_with_words is None else ignore_urls_with_words
    allow_only_with_words = [] if allow_only_with_words is None else allow_only_with_words
    extractor_options = {}
    if len(ignore_urls_with_words) > 0:
        ignored_words_regex = [re.compile(word) for word in ignore_urls_with_words]
        extractor_options['deny'] = ignored_words_regex

    if len(allow_only_with_words) > 0:
        allow_only_words_regex = [re.compile(word) for word in allow_only_with_words]
        extractor_options['allow'] = allow_only_words_regex
    extractor = LinkExtractor(**extractor_options)
    rules = [
        # Rule(extractor, callback='parse_item', follow=follow)
        Rule(extractor, follow=follow)
    ]
    domain = url.split("://")[1].split("/")[0]  # TODO - clean this

    if parser_config:
        spider_cls = InvanaWebsiteParserSpider
    else:
        spider_cls = InvanaWebsiteSpider
    spider_kwargs = {
        "start_urls": [url],
        "allowed_domains": [domain],
        "rules": rules,
        "parser_config": parser_config,
        "context": context
    }

    return spider_cls, spider_kwargs


def crawl_feeds(feed_urls=None, settings=None):
    """

    :param feed_urls:
    :param settings:
    :return:
    """
    if settings is None:
        settings = {}
    settings['TELNETCONSOLE_PORT'] = None
    process = CrawlerProcess(settings)
    allowed_domains = []
    for feed_url in feed_urls:
        domain = feed_url.split("://")[1].split("/")[0]  # TODO - clean this
        allowed_domains.append(domain)

    process.crawl(RSSSpider,
                  start_urls=feed_urls,
                  )
    process.start()

#
# def crawler(config=None,
#             settings=None):
#     """
#     DEPRECATED IN FAVOUR OF merging into InvanaBot
#     Crawl the site and apply a parser on top of it.
#     :param config:
#     :param settings:
#     :return:
#     """
#     if settings is None:
#         settings = {
#             'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
#         }
#     if "USER_AGENT" not in settings.keys():
#         settings['USER_AGENT'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'  # TODO - make this random
#     validate_config(config=config)
#     config = process_config(config)
#     settings['TELNETCONSOLE_PORT'] = None
#     process = CrawlerProcess(settings)
#
#     process.crawl(InvanaWebsiteParserSpider,
#                   start_urls=[config.get('start_url')],
#                   name=config.get('crawler_name'),
#                   parser_config=config
#                   )
#     process.start()
