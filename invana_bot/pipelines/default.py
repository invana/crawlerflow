from invana_bot.spiders.default import DefaultParserSpider
from scrapy.linkextractors import LinkExtractor
from invana_bot.utils.crawlers import get_crawler_from_list
from invana_bot.utils.config import validate_cti_config
from scrapy.spiders import Rule


class ParserCrawler(object):
    """

    pipe_data = {  # single pipe

        "crawler_id": "blog-list",
        "parsers": [
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

    def __init__(self, current_crawler=None, start_urls=None, job_id=None,
                 crawlers=None, context=None):
        """

        :param current_crawler: single crawler in the CTI flow
        :param crawlers: all the crawlers in the CTI flow
        :param context: any extra information user want to send to the crawled data or carry forward.
        """
        self.current_crawler = current_crawler
        self.job_id = job_id
        self.crawlers = crawlers
        self.start_urls = start_urls
        if context:
            self.context = context
        self.validate_pipe()

    def validate_pipe(self):
        must_have_keys = ["crawler_id", "parsers"]
        optional_keys = ["traversals"]
        for key in must_have_keys:
            if key not in self.current_crawler.keys():
                raise Exception(
                    "invalid parser data, should have the following keys; {}".format(",".join(must_have_keys)))

    def validate_traversal(self):
        pass  # TODO - implement this

    def validate_extractor(self):
        pass  # TODO - implement this

    def get_traversals(self):
        return self.current_crawler.get("traversals", [])

    def get_extractors(self):
        return self.current_crawler.get("parsers", [])

    def generate_pipe_kwargs(self):
        domains = []

        for url in self.start_urls:
            domain = url.split("://")[1].split("/")[0]  # TODO - clean this
            domains.append(domain)

        extractor = LinkExtractor()
        rules = [
            Rule(extractor, follow=True)  # TODO - add regex types of needed.
        ]

        spider_kwargs = {
            "start_urls": self.start_urls,
            "allowed_domains": domains,
            "rules": rules,
            "current_crawler": self.current_crawler,
            "crawlers": self.crawlers,
            "context": self.context
        }
        return spider_kwargs

    def run(self):
        spider_cls = DefaultParserSpider
        spider_kwargs = self.generate_pipe_kwargs()
        return {"spider_cls": spider_cls, "spider_kwargs": spider_kwargs}


class CTIRunner(object):
    """


    """

    def __init__(self, cti_manifest=None, job_id=None, context=None):
        self.cti_manifest = cti_manifest
        self.crawlers = self.cti_manifest['crawlers']
        self.job_id = job_id
        self.context = context

    def run(self):
        validate_cti_config(config=self.cti_manifest)
        initial_crawler = get_crawler_from_list(crawler_id=self.cti_manifest['init_data']['crawler_id'],
                                                crawlers=self.crawlers)
        print("initial_crawler", initial_crawler)
        parser_crawler = ParserCrawler(
            job_id=self.job_id,
            start_urls=self.cti_manifest['init_data']['start_urls'],
            current_crawler=initial_crawler,
            crawlers=self.crawlers,
            context=self.context
        )
        cti_job = parser_crawler.run()
        return cti_job
