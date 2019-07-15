from invana_bot.utils.spiders import get_crawler_from_list
from invana_bot.engines.single import SingleCrawlerRunnerEngine
from invana_bot.utils.config import validate_cti_config
from .base import RunnerEngineBase


class CTIFlowRunnerEngine(RunnerEngineBase):
    """

    CTIFlowRunnerEngine


    """

    def __init__(self, cti_manifest=None, settings=None, job_id=None,
                 context=None, crawler_cls=None,
                 extra_arguments=None):
        self.manifest = cti_manifest
        self.settings = settings
        # print("settings", settings)
        self.spiders = self.manifest['spiders']
        self.job_id = job_id
        self.context = context
        self.crawler_cls = crawler_cls
        self.extra_arguments = extra_arguments

    def crawl(self):
        errors = validate_cti_config(self.manifest)
        if len(errors) == 0:

            initial_crawler = get_crawler_from_list(
                spider_id=self.manifest['init_crawler']['spider_id'],
                spiders=self.spiders
            )
            initial_crawler['start_urls'] = self.manifest['init_crawler']['start_urls']
            crawler_runner = SingleCrawlerRunnerEngine(
                job_id=self.job_id,
                current_crawler=initial_crawler,
                spiders=self.spiders,
                context=self.context,
                crawler_cls=self.crawler_cls,
                settings=self.settings,
                extra_arguments=self.extra_arguments
            )
            cti_job = crawler_runner.run()

            return cti_job, errors
        else:
            return None, errors
