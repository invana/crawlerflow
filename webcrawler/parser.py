"""
Look at https://doc.scrapy.org/en/latest/topics/practices.html for usage

"""
import scrapy
from scrapy.crawler import CrawlerProcess
from .exceptions import NotImplemented


def validate_config(config=None):
    # TODO - help check if all the keys exist and the data types match for the crawler needs
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


def make_selector(html_element, selector, ):
    if selector.get('selector_attribute') in ['text']:
        if selector.get('selector_type') == 'css':
            elems = html_element.css("{0}:{1}".format(selector.get('selector'),
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
    if settings is None:
        settings = {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        }
    if "USER_AGENT" not in settings.keys():
        settings['USER_AGENT'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
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
            for selector in config['data_selectors']:
                if selector.get('selector_attribute') == 'element' and \
                        len(selector.get('child_selectors', [])) > 0:
                    # TODO - currently only support multiple elements strategy. what if multiple=False
                    elements = response.css(selector.get('selector'))
                    elements_data = []
                    for el in elements:
                        datum = {}
                        for child_selector in selector.get('child_selectors', []):
                            if child_selector.get('selector_attribute') == 'html':
                                selector_text = child_selector.get('selector')
                                _d = el.css(selector_text).extract_first()
                            else:
                                _d = el.css("{0}::{1}".format(child_selector.get('selector'),
                                                         child_selector.get('selector_attribute'))).extract_first()
                            datum[child_selector.get('id')] = _d.strip() if _d else None
                            elements_data.append(datum)
                    data[selector.get('id')] = elements_data

                else:
                    data[selector.get('id')] = response.css("{0}::{1}".format(
                        selector.get('selector'), selector.get('selector_attribute'))).extract_first()

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
