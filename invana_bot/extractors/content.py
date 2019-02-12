from invana_bot.extractors.base import ExtractorBase
from invana_bot.utils.selectors import get_selector_element


class MetaTagsExtractor(ExtractorBase):
    # TODO - implement this
    pass


class ParagraphsExtractor(ExtractorBase):
    # TODO - implement this
    def run(self):
        data = {}
        paragraphs_data = []
        elements = self.response.css("p").extract()
        for el in elements:
            paragraphs_data.append(el)
        data[self.__class__.__name__] = paragraphs_data

        return data


class HeadingsExtractor(ExtractorBase):
    # TODO - implement this
    pass


class MainContentExtractor(ExtractorBase):
    # TODO - implement this
    pass


class TableContentExtractor(ExtractorBase):
    # TODO - implement this
    pass


class CustomContentExtractor(ExtractorBase):
    # TODO - implement this
    def run(self):
        data = {}
        data['url'] = self.response.url
        for selector in self.extractor.get('data_selectors', []):
            if selector.get('selector_attribute') == 'element' and len(selector.get('child_selectors', [])) > 0:
                # TODO - currently only support multiple elements strategy. what if multiple=False
                elements = self.response.css(selector.get('selector'))
                elements_data = []
                for item_no, el in enumerate(elements):
                    item_no = item_no + 1  # because enumerate starts from 0
                    datum = {}
                    for child_selector in selector.get('child_selectors', []):
                        _d = get_selector_element(el, child_selector)
                        datum[child_selector.get('id')] = _d.strip() if _d else None
                    datum['item_no'] = item_no
                    elements_data.append(datum)
                print ("====+++++++++++", selector)
                if selector.get("multiple", False) is False:
                    data[selector.get('id')] = elements_data[0]
                else:
                    data[selector.get('id')] = elements_data
            else:
                _d = get_selector_element(self.response, selector)
                data[selector.get('id')] = _d.strip() if _d else None
        return data
