from invana_bot.crawlers.default import InvanaBotSingleWebCrawler
from scrapy.spiders import Rule
from invana_bot.utils.config import validate_crawler_config
from scrapy.linkextractors import LinkExtractor
from .base import RunnerEngineBase


class SingleCrawlerRunnerEngine(RunnerEngineBase):
    """

SingleCrawlerRunnerEngine
    crawler = {  # single pipe

        "crawler_id": "blog-list",
        "parsers": [
            {
                "data_selectors": [
                    {
                        "id": "items",
                        "selector": ".post-listing .post-item",
                        "selector_attribute": "element",
                        "multiple": True
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
        }],
        "context":{
        },
        "settings": {
        }

    }

    """

    def __init__(self,
                 current_crawler=None,
                 crawlers = None,
                 job_id=None,
                 context=None,
                 crawler_cls=None,
                 settings=None
                 ):
        """

        :param current_crawler: single crawler in the CTI flow
        :param crawlers: all the crawlers in the CTI flow
        :param context: any extra information user want to send to the crawled data or carry forward.
        :param settings:  settings to run the crawling job. .
        """
        self.manifest = current_crawler
        self.job_id = job_id
        if crawlers is None:
            self.crawlers = [current_crawler]
        else:
            self.crawlers = crawlers
        self.settings = settings
        self.crawler_cls = crawler_cls
        if context:
            self.context = context

    def crawl(self):
        errors = validate_crawler_config(self.manifest)
        if len(errors) == 0:

            cti_job = self.run()

            return cti_job, errors
        else:
            return None, errors

    def validate_pipe(self):
        must_have_keys = ["crawler_id", "parsers"]
        optional_keys = ["traversals"]
        for key in must_have_keys:
            if key not in self.manifest.keys():
                raise Exception(
                    "invalid parser data, should have the following keys; {}".format(",".join(must_have_keys)))

    def validate_traversal(self):
        pass  # TODO - implement this

    def validate_extractor(self):
        pass  # TODO - implement this

    def get_traversals(self):
        return self.manifest.get("traversals", [])

    def get_extractors(self):
        return self.manifest.get("parsers", [])

    def generate_crawler_kwargs(self):
        extractor = LinkExtractor()
        rules = [
            Rule(extractor, follow=True)  # TODO - add regex types of needed.
        ]
        allowed_domains = self.manifest.get("settings", {}).get('allowed_domains', [])
        crawler_kwargs = {
            "start_urls": self.manifest['start_urls'],
            "allowed_domains": allowed_domains,
            "rules": rules,
            "current_crawler": self.manifest,
            "crawlers": self.crawlers,
            "context": self.context
        }
        return crawler_kwargs

    def run(self):
        crawler_cls = self.crawler_cls or InvanaBotSingleWebCrawler

        crawler_kwargs = self.generate_crawler_kwargs()
        return {"crawler_cls": crawler_cls, "crawler_kwargs": crawler_kwargs, "spider_settings": self.settings}
