from invana_bot.spiders.default import DefaultPipeletSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class WebCrawlerPipelet(object):
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

    def __init__(self, pipe=None, start_urls=None, job_id=None,
                 pipeline=None, context=None):
        """

        :param pipe: single unit of crawling
        :param pipeline: set of units combined to create a flow
        :param context: any extra information user want to send to the crawled data.
        """
        self.pipe = pipe
        self.job_id = job_id
        self.crawlers = pipeline
        self.start_urls = start_urls
        if context:
            self.context = context
        self.validate_pipe()

    def validate_pipe(self):
        must_have_keys = ["parser_id", "data_extractors"]
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

    def get_extractors(self):
        return self.pipe.get("data_extractors", [])

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
            "pipe": self.pipe,
            "pipeline": self.crawlers,
            "context": self.context
        }
        return spider_kwargs

    def run(self):
        spider_cls = DefaultPipeletSpider
        spider_kwargs = self.generate_pipe_kwargs()
        return {"spider_cls": spider_cls, "spider_kwargs": spider_kwargs}


class CTIRunner(object):
    """



    """

    def __init__(self, cti_config=None, job_id=None, context=None):
        self.cti_config = cti_config
        self.crawlers = self.cti_config['crawlers']
        self.job_id = job_id
        self.context = context

    def get_pipelet(self, pipe_id=None):
        pipeline = self.crawlers['crawlers']
        for pipe in pipeline:
            if pipe.get("pipe_id") == pipe_id:
                return pipe
        return

    def run(self):
        pipe = self.crawlers[0]
        invana_pipe = WebCrawlerPipelet(pipe=pipe,
                                        start_urls=pipe['start_urls'],
                                        job_id=self.job_id,
                                        pipeline=self.crawlers,
                                        context=self.context)
        job = invana_pipe.run()
        return job
