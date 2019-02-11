from invana_bot.spiders.base import InvanaWebsiteSpiderBase
from invana_bot.utils.selectors import get_selector_element
from invana_bot.utils.url import get_urn, get_domain
import scrapy
from invana_bot.utils.config import validate_config, process_config
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


def process_parser(self, extractor=None):
    extractor_cleaned = None
    if extractor:
        is_valid_config = validate_config(config=extractor)
        if is_valid_config:
            if extractor.get("is_processed") == True:
                extractor_cleaned = extractor
                return extractor_cleaned
            else:
                extractor_cleaned = process_config(extractor)
                extractor_cleaned['is_processed'] = True
        else:
            raise Exception("invalid parser config")
    return extractor_cleaned


class DefaultInvanaPipeSpider(InvanaWebsiteSpiderBase):
    """
    This is generic spider
    """
    name = "DefaultInvanaPipeline"

    def closed(self, reason):
        print("spider closed with payload:", reason, self.pipe)

    def run_extractor(self, response=None, extractor=None, ):
        context = self.context
        data = {}
        data['url'] = response.url
        for selector in extractor.get('data_selectors', []):
            if selector.get('selector_attribute') == 'element' and len(selector.get('child_selectors', [])) > 0:
                # TODO - currently only support multiple elements strategy. what if multiple=False
                elements = response.css(selector.get('selector'))
                elements_data = []
                for item_no, el in enumerate(elements):
                    item_no = item_no + 1  # because enumerate starts from 0
                    datum = {}
                    for child_selector in selector.get('child_selectors', []):
                        _d = get_selector_element(el, child_selector)
                        datum[child_selector.get('id')] = _d.strip() if _d else None
                    datum['item_no'] = item_no
                    elements_data.append(datum)
                data[selector.get('id')] = elements_data
            else:
                _d = get_selector_element(response, selector)
                data[selector.get('id')] = _d.strip() if _d else None
        if context is not None:
            data.update({"context": context})
        return data

    # def run_pagination_traversal(self, response=None, traversal=None):

    def parse(self, response=None):
        pipe = self.pipe
        for extractor in pipe['data_extractors']:
            data = self.run_extractor(response=response, extractor=extractor, )
            yield data

        for traversal in pipe['traversals']:
            print("traversal", traversal)
            if traversal['traversal_type'] == "pagination":
                pagination = traversal['pagination']
                max_pages = pagination.get("max_pages", 1)
                current_page_count = response.meta.get('current_page_count', 1)
                print("max_pages", max_pages, current_page_count)
                if current_page_count < max_pages:
                    next_selector = pagination.get('selector')
                    if next_selector:
                        if pagination.get('selector_type') == 'css':
                            next_page = response.css(next_selector + "::attr(href)").extract_first()
                        elif pagination.get('selector_type') == 'xpath':
                            next_page = response.xpath(next_selector + "::attr(href)").extract_first()
                        else:
                            next_page = None
                        current_page_count = current_page_count + 1
                        if next_page:
                            if not "://" in next_page:
                                next_page_url = "https://" + get_domain(response.url) + next_page
                            else:
                                next_page_url = next_page
                            yield scrapy.Request(
                                next_page_url, callback=self.parse,
                                meta={"current_page_count": current_page_count}
                            )


class DefaultInvanaPipeline(object):

    def __init__(self, pipeline_data=None):
        self.pipeline_data = pipeline_data

    def create_pipe(self, pipe=None):
        print("pipe_application")
        domains = []
        for url in pipe['start_urls']:
            domain = url.split("://")[1].split("/")[0]  # TODO - clean this
            domains.append(domain)

        extractor = LinkExtractor()
        rules = [
            Rule(extractor, follow=True)
        ]

        context = self.pipeline_data['context']
        spider_kwargs = {
            "start_urls": pipe['start_urls'],
            "allowed_domains": domains,
            "rules": rules,
            "pipe": pipe,
            "context": context
        }
        return spider_kwargs

    def run(self):
        jobs = []
        for pipe in self.pipeline_data['pipeline']:
            print("pipe", pipe['pipe_id'])
            spider_cls = DefaultInvanaPipeSpider
            spider_kwargs = self.create_pipe(pipe=pipe)
            jobs.append([spider_cls, spider_kwargs])
        return jobs
