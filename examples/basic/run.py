from invana_bot.crawlers.generic import InvanaBotWebCrawler
from invana_bot.settings import DEFAULT_SETTINGS
from invana_bot.managers.manifest import ETIManifestManager
import eti_transformations

if __name__ == '__main__':
    manifest_manager = ETIManifestManager(cti_config_path="./", eti_transformations_module=eti_transformations)
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
