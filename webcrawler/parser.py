"""
Look at https://doc.scrapy.org/en/latest/topics/practices.html for usage

"""
import scrapy
from scrapy.crawler import CrawlerProcess
from .exceptions import NotImplemented, InvalidCrawlerConfig
from webcrawler.spiders.website import InvanaWebsiteSpider
from webcrawler.spiders.generic import InvaanaGenericSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import re


def validate_config(config=None):
    required_keys = ['crawler_name', 'domain', 'subdomain', 'start_url', 'data_selectors']
    for key_ in required_keys:
        if key_ not in config.keys():
            InvalidCrawlerConfig("Invalid configuration: Required Key {0} not found in the configuration".format(key_))
    # TODO - validate all the data_selectors data aswell
    return True


def process_config(config=None):
    processed_config_dict = {}
    parent_selectors = []
    new_config_selectors = []
    for selector in config['data_selectors']:
        if selector.get('selector_attribute') == 'element':
            parent_selectors.append(selector)

    """
    process the element root selectors (without parent_selector) which might become dictionaries
    """
    if len(parent_selectors) > 0:
        for parent_selector in parent_selectors:
            processed_config_dict[parent_selector.get('id')] = parent_selector
            processed_config_dict[parent_selector.get('id')]['child_selectors'] = []

            for selector in config['data_selectors']:
                if selector.get('parent_selector') == parent_selector.get('id'):
                    processed_config_dict[parent_selector.get('id')]['child_selectors'].append(selector)

    """
    process the elements with no root selectors
    """
    for selector in config['data_selectors']:
        if selector.get('parent_selector') is None and selector.get('selector_attribute') != 'element':
            new_config_selectors.append(selector)

    for k, v in processed_config_dict.items():
        new_config_selectors.append(v)
    config['data_selectors'] = new_config_selectors
    return config


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
