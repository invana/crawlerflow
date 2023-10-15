from .base import SpiderBase
import importlib


class HTMLSpider(SpiderBase):
    """

    """

    def run_extractor(self, response, extractor_type, exctactor_fields=None):
        extractor_cls = getattr(importlib.import_module(
            f"crawlerflow.extractors"), extractor_type)
        extractor = extractor_cls(response, extractor_fields=exctactor_fields)
        return extractor.extract()

    def parse_default_extractor(self, response):
        return self.run_extractor(response, self.default_extractor['extractor_type'], exctactor_fields=self.default_extractor.get('fields', {}))

    def parse_other_extractors(self, response):
        data = {}
        for extractor_id, single_extractor_config in self.other_extractors.items():
            # extractor_cls = getattr(importlib.import_module(f"crawlerflow.extractors"), single_extractor_config['extractor_type'])
            # extractor = extractor_cls(response, single_extractor_config['fields'] )

            extractor = self.run_extractor(
                response, single_extractor_config['extractor_type'], exctactor_fields=single_extractor_config.get('fields', {}))
            data[extractor_id] = extractor.extract()
        return data
