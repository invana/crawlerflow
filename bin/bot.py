import sys
import os

sys.path.append('../')
from invana_bot.crawlers.generic import InvanaBotWebCrawler
from invana_bot.settings import DEFAULT_SETTINGS
from invana_bot.managers.manifest import ETIManifestManager

path = os.path.abspath('../examples/basic')

print("path", path)
manifest_manager = ETIManifestManager(
    cti_config_path=path
)
cti_manifest = manifest_manager.get_manifest()
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
