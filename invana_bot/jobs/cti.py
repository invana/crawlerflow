from .base import InvanaBotJobGeneratorBase
from invana_bot.core.engines.cti import InvanaBotRunnerEngine
from datetime import datetime


class InvanaBotJobGenerator(InvanaBotJobGeneratorBase):
    """
        Invana-bot cti job generator
    """

    # def create_job(self,
    #                spider_config=None,
    #                context=None,
    #                spider_cls=None):
    #     if context is None:
    #         context = {}
    #     if 'job_id' not in context.keys():
    #         context['job_id'] = self.job_id
    #         context['job_started'] = datetime.now()
    #
    #     settings_from_manifest = spider_config.get("settings", {})
    #     actual_settings = self.settings
    #     actual_settings['DOWNLOAD_DELAY'] = settings_from_manifest.get("download_delay", 0)
    #     runner = CrawlerRunnerEngineBase(settings=actual_settings,
    #                                  spider_config=spider_config,
    #                                  job_id=self.job_id,
    #                                  context=context,
    #                                  spider_cls=spider_cls)
    #     job, errors = runner.crawl()
    #     return {"spider_job": job, "spider_job_errors": errors, "runner": runner}
    #

    def create_job(self, manifest=None, context=None, spider_cls=None, extra_arguments=None):
        if context is None:
            context = {}
        if 'job_id' not in context.keys():
            context['job_id'] = self.job_id
            context['job_started'] = datetime.now()

        settings_from_manifest = manifest.get("settings", {})
        print("============")
        print("============")
        print(settings_from_manifest)

        actual_settings = self.settings
        for k, v in settings_from_manifest.items():
            actual_settings[k.upper()] = v
        print(actual_settings)
        print("============")
        print("============")

        # actual_settings['DOWNLOAD_DELAY'] = settings_from_manifest.get("download_delay", 0)
        # actual_settings['ALLOWED_DOMAINS'] = settings_from_manifest.get("allowed_domains", [])
        runner = InvanaBotRunnerEngine(
            job_id=self.job_id,
            spider_cls=spider_cls,
            manifest=manifest,

            # settings=actual_settings,
            # context=context,
            # extra_arguments=extra_arguments
        )
        job, errors = runner.crawl()
        print("<<<<<<<<<<<<<<<<<<<<<<<=======", )
        print("<<<<<<<<<<<<<<<<<<<<<<<=======", )
        print("job errors", errors)
        print("<<<<<<<<<<<<<<<<<<<<<<<=======", )
        print("<<<<<<<<<<<<<<<<<<<<<<<=======", )
        job["spider_settings"] = actual_settings
        # job["spider_kwargs"]["default_storage"] = self.get_default_storage(settings=actual_settings)
        return {"spider_job": job, "spider_job_errors": errors, "runner": runner}
