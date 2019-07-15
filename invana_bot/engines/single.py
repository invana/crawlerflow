from invana_bot.spiders.web import InvanaBotSingleWebCrawler
from scrapy.spiders import Rule
from invana_bot.utils.config import validate_crawler_config
from scrapy.linkextractors import LinkExtractor
from .base import RunnerEngineBase


class SingleCrawlerRunnerEngine(RunnerEngineBase):
    """

SingleCrawlerRunnerEngine
    crawler = {  # single pipe

        "spider_id": "blog-list",
        "extractors": [
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
                 spiders=None,
                 job_id=None,
                 context=None,
                 crawler_cls=None,
                 settings=None,
                 extra_arguments=None
                 ):
        """

        :param current_crawler: single crawler in the CTI flow
        :param spiders: all the spiders in the CTI flow
        :param context: any extra information user want to send to the crawled data or carry forward.
        :param extra_arguments: extra parameters that you want to send to spider class
        :param settings:  settings to run the crawling job. .
        """
        self.manifest = current_crawler
        self.job_id = job_id
        if spiders is None:
            self.spiders = [current_crawler]
        else:
            self.spiders = spiders
        self.settings = settings
        self.crawler_cls = crawler_cls
        self.extra_arguments = extra_arguments or {}
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
        must_have_keys = ["spider_id", "extractors"]
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
        return self.manifest.get("extractors", [])

    def generate_crawler_kwargs(self):
        extractor = LinkExtractor()
        rules = [
            Rule(extractor, follow=True)  # TODO - add regex types of needed.
        ]
        # allowed_domains = self.settings.get('allowed_domains', [])
        crawler_kwargs = {
            "start_urls": self.manifest['start_urls'],
            "allowed_domains": [],
            # NOTE - allowed_domains  is going flexible on this because this is a general crawl start,
            #

            "rules": rules,
            "current_crawler": self.manifest,
            "spiders": self.spiders,
            "context": self.context,

        }
        crawler_kwargs.update(self.extra_arguments)
        return crawler_kwargs

    def run(self):
        crawler_cls = self.crawler_cls or InvanaBotSingleWebCrawler

        crawler_kwargs = self.generate_crawler_kwargs()
        return {"crawler_cls": crawler_cls, "crawler_kwargs": crawler_kwargs, "spider_settings": self.settings}
