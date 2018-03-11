"""
Look at https://doc.scrapy.org/en/latest/topics/practices.html for usage

"""
import scrapy
from scrapy.crawler import CrawlerProcess
from .exceptions import NotImplemented, InvalidCrawlerConfig
from datetime import datetime
from webcrawler.spiders.website import InvanaWebsiteSpider


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


def get_domain(url):
    pass


def get_selector_element(html_element, selector, ):
    if selector.get('selector_attribute') in ['text']:
        if selector.get('selector_type') == 'css':
            elems = html_element.css("{0}::{1}".format(selector.get('selector'),
                                                       selector.get('selector_attribute')))
            return elems if selector.get('multiple') else elems.extract_first()
        else:
            raise NotImplemented("selector_type not equal to css; this is not implemented")
    elif selector.get('selector_attribute') == 'html':
        if selector.get('selector_type') == 'css':
            elems = html_element.css(selector.get('selector'))
            return elems if selector.get('multiple') else elems.extract_first()
        else:
            raise NotImplemented("selector_type not equal to css; this is not implemented")
    else:
        if selector.get('selector_type') == 'css':
            elems = html_element.css(selector.get('selector')) \
                .xpath("@{0}".format(selector.get('selector_attribute')))
            return elems if selector.get('multiple') else elems.extract_first()
        else:
            raise NotImplemented("selector_type not equal to css; this is not implemented")


def crawler(config=None, settings=None):
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

    class InvaanaGenericSpider(scrapy.Spider):
        name = config.get('crawler_name')
        # allowed_domains = [] TODO
        start_urls = [
            config.get('start_url')
        ]

        def parse(self, response):
            data = {}
            data['url'] = response.url
            for selector in config['data_selectors']:
                if selector.get('selector_attribute') == 'element' and \
                        len(selector.get('child_selectors', [])) > 0:
                    # TODO - currently only support multiple elements strategy. what if multiple=False
                    elements = response.css(selector.get('selector'))
                    elements_data = []
                    for el in elements:
                        datum = {}
                        for child_selector in selector.get('child_selectors', []):
                            _d = get_selector_element(el, child_selector)
                            datum[child_selector.get('id')] = _d.strip() if _d else None
                            elements_data.append(datum)
                    data[selector.get('id')] = elements_data
                else:
                    _d = get_selector_element(response, selector)
                    data[selector.get('id')] = _d.strip() if _d else None
            yield data

            next_selector = config.get('next_page_selector').get('selector')
            if next_selector:
                if config.get('next_page_selector').get('selector_type') == 'css':
                    next_pages = response.css(next_selector)
                elif config.get('next_page_selector').get('selector_type') == 'xpath':
                    next_pages = response.xpath(next_selector)
                else:
                    next_pages = []
                for next_page in next_pages:
                    yield response.follow(next_page, self.parse)

    process.crawl(InvaanaGenericSpider)
    process.start()


def crawl_website(url=None, settings=None):
    process = CrawlerProcess(settings)

    process.crawl(InvanaWebsiteSpider)
    process.start()
