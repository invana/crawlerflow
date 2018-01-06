"""
Look at https://doc.scrapy.org/en/latest/topics/practices.html for usage

"""
import scrapy
from scrapy.crawler import CrawlerProcess


def validate_config(config=None):
    # TODO - help check if all the keys exist and the data types match for the crawler needs
    return True


def process_config(config=None):
    processed_config_dict = {}
    parent_selectors = []
    new_config = []
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
            new_config.append(selector)

    for k, v in processed_config_dict.items():
        new_config.append(v)

    return new_config


def get_domain(url):
    pass


def crawler(config=None, settings=None):
    if settings is None:
        settings = {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        }
    if "USER_AGENT" not in settings.keys():
        settings['USER_AGENT'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    process_config(config)
    process = CrawlerProcess(settings)

    class InvaanaGenericSpider(scrapy.Spider):
        name = config.get('crawler_name')
        # allowed_domains = [] TODO
        start_urls = [
            config.get('start_url')
        ]

        def parse(self, response):
            data = {}
            for title in response.css('h2.entry-title'):
                yield {'title': title.css('a ::text').extract_first()}

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
