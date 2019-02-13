from invana_bot.spiders.default import DefaultPipeletSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from invana_bot.utils.config import validate_config, process_config


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

    def get_extractors(self):
        return self.pipe.get("data_extractors", [])

    def generate_pipe_kwargs(self):
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


class WebCrawlerPipeline(object):
    """



    """

    def __init__(self, pipeline=None, job_id=None):
        self.pipeline = pipeline
        self.job_id = job_id
        self.validate_pipeline()

    def process_parser(self, parser_config=None):
        return process_config(parser_config)

    def validate_pipeline(self):
        for pipe in self.pipeline['pipeline']:
            for extractor in pipe.get('data_extractors', []):
                extractor['data_selectors'] = self.process_parser(extractor)['data_selectors']

    def get_pipelet(self, pipe_id=None):
        pipeline = self.pipeline['pipeline']
        for pipe in pipeline:
            if pipe.get("pipe_id") == pipe_id:
                return pipe
        return

    def run(self):
        jobs = []
        for pipe in self.pipeline['pipeline']:
            if pipe.get("start_urls"):
                print("Starting the pipelet: [{}]".format(pipe['pipe_id']))

                invana_pipe = WebCrawlerPipelet(pipe=pipe, pipeline=self.pipeline)
                spider_cls = DefaultPipeletSpider
                spider_kwargs = invana_pipe.generate_pipe_kwargs()
                jobs.append([spider_cls, spider_kwargs])
            else:
                print(
                    "Ignoring initiating the pipelet: [{}] as it doesn't "
                    "have start_urls; must be next step of other pipeline".format(
                        pipe["pipe_id"]))
        return jobs
