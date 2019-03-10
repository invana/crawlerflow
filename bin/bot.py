# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import argparse

sys.path.append('../')
from invana_bot.crawlers.generic import InvanaBotWebCrawler
from invana_bot.settings import DEFAULT_SETTINGS
from invana_bot.managers.manifest import ETIManifestManager

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='InvanaBot - A web crawler framework that can'
                                                 ' transform websites into datasets with Crawl, '
                                                 'Transform and Index workflow. ')

    parser.add_argument('--path', type=str, default='./', help='FOO!')

    args = parser.parse_args()
    path = os.path.abspath(args.path)
    manifest_manager = ETIManifestManager(
        cti_config_path=path
    )
    cti_manifest, errors = manifest_manager.get_manifest()
    if len(errors) == 0:
        crawler = InvanaBotWebCrawler(
            settings=DEFAULT_SETTINGS
        )
        context = cti_manifest.get("context")
        job = crawler.create_job(
            cti_manifest=cti_manifest,
            context=context
        )
        print("job", job)
        crawler.start_job(job=job)
    else:
        print("==============================================================")
        print("ERROR : The path {} doesnt have the required files and failing with the errors {}".format(
            manifest_manager.cti_config_path,
            errors
        ))
        print("==============================================================")
