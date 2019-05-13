from invana_bot.utils.crawlers import get_crawler_from_list
from invana_bot.engines.single import SingleCrawlerRunnerEngine
from invana_bot.utils.config import validate_cti_config
from .base import RunnerEngineBase


class CTIFlowRunnerEngine(RunnerEngineBase):
    """

    CTIFlowRunnerEngine


    """

    def __init__(self, cti_manifest=None, settings=None, job_id=None, context=None, crawler_cls=None):
        self.manifest = cti_manifest
        self.settings = settings
        self.crawlers = self.manifest['crawlers']
        self.job_id = job_id
        self.context = context
        self.crawler_cls = crawler_cls

    def crawl(self):
        errors = validate_cti_config(self.manifest)
        if len(errors) == 0:

            initial_crawler = get_crawler_from_list(
                crawler_id=self.manifest['init_crawler']['crawler_id'],
                crawlers=self.crawlers
            )
            initial_crawler['start_urls'] = self.manifest['init_crawler']['start_urls']
            crawler_runner = SingleCrawlerRunnerEngine(
                job_id=self.job_id,
                current_crawler=initial_crawler,
                crawlers=self.crawlers,
                context=self.context,
                crawler_cls=self.crawler_cls,
                settings=self.settings
            )
            cti_job = crawler_runner.run()

            return cti_job, errors
        else:
            return None, errors
