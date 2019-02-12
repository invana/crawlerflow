from invana_bot.spiders.base import InvanaWebsiteSpiderBase
from invana_bot.utils.selectors import get_selector_element
from invana_bot.utils.url import get_domain
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from invana_bot.utils.config import validate_config, process_config


class InvanaCrawlerPipe(object):
    """

    pipe_data = {  # single pipe

        "pipe_id": "blog-list",
        "start_urls": ["https://blog.scrapinghub.com"],
        "data_extractors": [
            {
                "data_selectors": [
                    {
                        "id": "items",
                        "selector": ".post-listing .post-item",
                        "selector_attribute": "element",
                        "multiple": True
                    },
                    {
                        "id": "url",
                        "selector": ".post-header h2 a",
                        "selector_type": "css",
                        "selector_attribute": "href",
                        "parent_selector": "items",
                        "multiple": False
                    },
                    {
                        "id": "title",
                        "selector": ".post-header h2 a",
                        "selector_type": "css",
                        "selector_attribute": "text",
                        "parent_selector": "items",
                        "multiple": False
                    },
                    {
                        "id": "content",
                        "selector": ".post-content",
                        "selector_type": "css",
                        "selector_attribute": "html",
                        "parent_selector": "items",
                        "multiple": False
                    }
                ],
            }
        ],
        "traversals": [{
            "traversal_type": "pagination",
            "pagination": {
                "selector": ".next-posts-link",
                "selector_type": "css",
                "max_pages": 2
            },
        }]

    }

    context = {
        "client_id": "something"
    }

    """

    def __init__(self, pipe=None, pipeline=None, context=None):
        """

        :param pipe: single unit of crawling
        :param pipeline: set of units combined to create a flow
        :param context: any extra information user want to send to the crawled data.
        """
        self.pipe = pipe
        self.pipeline = pipeline
        if context:
            self.context = context
        else:
            self.context = self.pipeline.get("context")
        self.validate_pipe()

    def validate_pipe(self):
        must_have_keys = ["pipe_id", "start_urls", "data_extractors"]
        optional_keys = ["traversals"]
        for key in must_have_keys:
            if key not in self.pipe.keys():
                raise Exception(
                    "invalid pipe data, should have the following keys; {}".format(",".join(must_have_keys)))

    def validate_traversal(self):
        pass  # TODO - implement this

    def validate_extractor(self):
        pass  # TODO - implement this

    def get_traversals(self):
        return self.pipe.get("traversals", [])

    def get_pipeline(self):
        return self.pipeline

    def get_extractors(self):
        return self.pipe.get("data_extractors", [])

    def get_pipe(self, pipe_id=None):
        pipeline = self.get_pipeline()
        for pipe in pipeline:
            if pipe.get("pipe_id") == pipe_id:
                return pipe
        return

    def generate_pipe_kwargs(self):
        print("pipe_application")
        domains = []

        for url in self.pipe['start_urls']:
            domain = url.split("://")[1].split("/")[0]  # TODO - clean this
            domains.append(domain)

        extractor = LinkExtractor()
        rules = [
            Rule(extractor, follow=True)  # TODO - add regex types of needed.
        ]

        spider_kwargs = {
            "start_urls": self.pipe['start_urls'],
            "allowed_domains": domains,
            "rules": rules,
            "pipe": self.pipe,
            "pipeline": self.pipeline,
            "context": self.context
        }
        return spider_kwargs


class DefaultInvanaPipeSpider(InvanaWebsiteSpiderBase):
    """
    This is generic spider
    """
    name = "DefaultInvanaPipeSpider"

    def closed(self, reason):
        print("spider closed with payload:", reason, self.pipe)

    def run_extractor(self, response=None, extractor=None):
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
                            # TODO - add logics to change the extractors or call a different pipe from here.
                            yield scrapy.Request(
                                next_page_url, callback=self.parse,
                                meta={"current_page_count": current_page_count}
                            )
            elif traversal['traversal_type'] == "something_else":
                pass


class DefaultInvanaPipeline(object):

    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.validate_pipeline()

    def process_parser(self, parser_config=None):
        return process_config(parser_config)

    def validate_pipeline(self):
        for pipe in self.pipeline['pipeline']:
            for extractor in pipe['data_extractors']:
                extractor['data_selectors'] = self.process_parser(extractor)['data_selectors']

    def run(self):
        jobs = []
        for pipe in self.pipeline['pipeline']:
            print("pipe", pipe['pipe_id'])
            invana_pipe = InvanaCrawlerPipe(pipe=pipe, pipeline=self.pipeline)
            spider_cls = DefaultInvanaPipeSpider
            spider_kwargs = invana_pipe.generate_pipe_kwargs()
            jobs.append([spider_cls, spider_kwargs])
        return jobs
