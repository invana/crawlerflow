# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import argparse
from invana_bot.jobs.cti import CTIJobGenerator
from invana_bot.jobs.single import SingleCrawlJobGenerator
from invana_bot.settings.default import DEFAULT_SETTINGS
from invana_bot.manifests.cti import CTIManifestManager
from invana_bot.manifests.single import SingleCrawlerManifestManager


def invana_bot_run():
    parser = argparse.ArgumentParser(description='InvanaBot - A web crawler framework that can'
                                                 ' transform websites into datasets with Crawl, '
                                                 'Transform and Index workflow. ')

    parser.add_argument('--path', type=str, default='./', help='FOO!')
    parser.add_argument('--type', type=str, default='cti', help='options are ct or single', choices=("single", "cti"))

    args = parser.parse_args()
    path = os.path.abspath(args.path)
    crawler_type = args.type
    # print("crawler_type", crawler_type)
    if crawler_type == "cti":
        manifest_manager = CTIManifestManager(
            cti_config_path=path
        )
        cti_manifest, errors = manifest_manager.get_manifest()
        if len(errors) == 0:
            crawler_job_generator = CTIJobGenerator(
                settings=DEFAULT_SETTINGS,
            )
            context = cti_manifest.get("context")
            job = crawler_job_generator.create_job(
                cti_manifest=cti_manifest,
                context=context
            )
            crawler_job_generator.start_job(job=job)
        else:
            print("==============================================================")
            print("ERROR : ETI Job Failing with the errors :: {}".format(
                manifest_manager.cti_config_path,
                errors
            ))
            print("==============================================================")
    elif crawler_type == "single":
        manifest_manager = SingleCrawlerManifestManager(
            config_path=path
        )
        crawler_manifest, errors = manifest_manager.get_manifest()
        if len(errors) == 0:
            crawler_job_generator = SingleCrawlJobGenerator(
                settings=DEFAULT_SETTINGS
            )
            context = crawler_manifest.get("context")
            job = crawler_job_generator.create_job(
                current_crawler=crawler_manifest,
                context=context
            )
            crawler_job_generator.start_job(job=job)
        else:
            print("==============================================================")
            print("ERROR : ETI Job Failing with the errors :: {}".format(
                manifest_manager.config_path,
                errors
            ))
            print("==============================================================")
