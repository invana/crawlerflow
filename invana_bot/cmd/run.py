# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import argparse
from invana_bot.jobs.cti import InvanaBotJobGenerator
from invana_bot.settings.default import DEFAULT_SETTINGS
from invana_bot.manifests.cti import CTIManifestManager
from invana_bot.spiders.web import InvanaBotSingleWebCrawler
from invana_bot.spiders.xml import GenericXMLFeedSpider
from invana_bot.spiders.api import GenericAPISpider
# from invana_bot.jobs.single import SingleCrawlJobGenerator
# from invana_bot.manifests.single import SingleCrawlerManifestManager


def invana_bot_run():
    crawler_choices = (
        "web",
        "web-single",
        "xml",
        "api"
    )
    parser = argparse.ArgumentParser(description='InvanaBot - A web crawler framework that can'
                                                 ' transform websites into datasets with Crawl, '
                                                 'Transform and Index workflow; just with the configuration.')

    parser.add_argument('--path', type=str, default='./', help='The path of the cti_manifest.yml')
    parser.add_argument('--type', type=str,
                        default='web',
                        required=True,
                        help='options are : {}'.format(",".join(crawler_choices)),
                        choices=crawler_choices)

    args = parser.parse_args()
    path = os.path.abspath(args.path)
    crawler_type = args.type

    if crawler_type == "web":
        spider_cls = InvanaBotSingleWebCrawler
    elif crawler_type == "xml":
        spider_cls = GenericXMLFeedSpider
    elif crawler_type == "api":
        spider_cls = GenericAPISpider

    else:
        raise Exception("There is no crawling strategy designed for crawler type: '{}'".format(crawler_type))

    manifest_manager = CTIManifestManager(
        cti_config_path=path
    )

    manifest, errors = manifest_manager.get_manifest()
    # print("cti_manifest", cti_manifest)

    first_crawler = manifest.get("spiders", [])[0]

    ignore_crawler_keys = ["spider_id", "allowed_domains", "extractors", "traversals"]
    extra_arguments = {}
    for k, v in first_crawler.items():
        if k not in ignore_crawler_keys:
            extra_arguments[k] = v
    if len(errors) == 0:
        spider_job_generator = InvanaBotJobGenerator(
            settings=DEFAULT_SETTINGS,
        )
        context = manifest.get("context")
        job = spider_job_generator.create_job(
            manifest=manifest,
            context=context,
            spider_cls=spider_cls,
            extra_arguments=extra_arguments

        )
        spider_job_generator.start_job(job=job)
    else:
        print("==============================================================")
        print("ERROR : ETI Job Failing with the errors :: {}".format(
            manifest_manager.cti_config_path,
            errors
        ))
        print("==============================================================")

        # manifest_manager = CTIManifestManager(
        #     cti_config_path=path
        # )
        # cti_manifest, errors = manifest_manager.get_manifest()
        # if len(errors) == 0:
        #     spider_job_generator = InvanaBotJobGenerator(
        #         settings=DEFAULT_SETTINGS,
        #     )
        #     context = cti_manifest.get("context")
        #     job = spider_job_generator.create_job(
        #         cti_manifest=cti_manifest,
        #         context=context
        #     )
        #     spider_job_generator.start_job(job=job)
        # else:
        #     print("==============================================================")
        #     print("ERROR : ETI Job Failing with the errors :: {}".format(
        #         manifest_manager.cti_config_path,
        #         errors
        #     ))
        #     print("==============================================================")
        #
    #
    # if crawler_type == "web-single":
    #     manifest_manager = SingleCrawlerManifestManager(
    #         config_path=path
    #     )
    #     crawler_manifest, errors = manifest_manager.get_manifest()
    #     if len(errors) == 0:
    #         spider_job_generator = SingleCrawlJobGenerator(
    #             settings=DEFAULT_SETTINGS
    #         )
    #         context = crawler_manifest.get("context")
    #         job = spider_job_generator.create_job(
    #             spider_config=crawler_manifest,
    #             context=context
    #         )
    #         spider_job_generator.start_job(job=job)
    #     else:
    #         print("==============================================================")
    #         print("ERROR : ETI Job Failing with the errors :: {}".format(
    #             manifest_manager.config_path,
    #             errors
    #         ))
    #         print("==============================================================")
