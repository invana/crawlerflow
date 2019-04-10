from invana_bot.extractors.base import ExtractorBase
from invana_bot.utils.selectors import get_selector_element


class AllLinksExtractor(ExtractorBase):
    def run(self):
        data = {}
        extracted_data = {}
        for selector in self.extractor.get('data_selectors', []):
            _d = get_selector_element(self.response, selector)
            extracted_data[selector.get('selector_id')] = _d
        data[self.parser_id] = extracted_data
        return data


class SameDomainLinkExtractor(ExtractorBase):
    pass


class ForeignDomainLinkExtractor(ExtractorBase):
    pass


class PaginationLinkExtractor(ExtractorBase):
    def run(self):
        data = {}
        extracted_data = {}
        for selector in self.extractor.get('data_selectors', []):
            _d = get_selector_element(self.response, selector)
            extracted_data[selector.get('selector_id')] = _d
        data[self.parser_id] = extracted_data
        return data


class CustomLinkExtractor(ExtractorBase):
    pass
