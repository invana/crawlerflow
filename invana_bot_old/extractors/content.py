from invana_bot.extractors.base import ExtractorBase
from invana_bot.utils.selectors import get_selector_element
import json


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
        data[self.parser_name] = paragraphs_data
        return data


class HeadingsExtractor(ExtractorBase):
    # TODO - implement this
    pass


class MainContentExtractor(ExtractorBase):
    # TODO - implement this
    pass


class TableContentExtractor(ExtractorBase):
    def run(self):
        data = {}
        tables = []
        for table in self.response.css("table"):
            table_data = []
            table_headers = [th.extract() for th in table.css("thead tr th::text")]
            for row in table.css("tbody tr"):
                row_data = [td.extract() for td in row.css("td::text")]
                row_dict = dict(zip(table_headers, row_data))
                table_data.append(row_dict)
            tables.append(table_data)
        data[self.parser_name] = tables
        return data


class HTMLMetaTagExtractor(ExtractorBase):
    def run(self):
        data = {}
        meta_data_dict = {}
        elements = self.response.css('meta')
        for element in elements:
            meta_property = element.xpath("@{0}".format('property')).extract_first()
            if meta_property:
                meta_property = meta_property.replace(":", "__")
                meta_data_dict[meta_property] = element.xpath("@{0}".format('content')).extract_first()

        data[self.parser_name] = meta_data_dict
        return data


class CustomContentExtractor(ExtractorBase):
    ITER_KEY = "iter_count"

    # TODO - implement this
    def run(self):
        data = {}
        extracted_data = {}
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
                        datum[child_selector.get('selector_id')] = _d.strip() if _d else None
                    datum[self.ITER_KEY] = item_no
                    elements_data.append(datum)
                if selector.get("multiple", False) is False:
                    single_data = elements_data[0]
                    single_data.pop(self.ITER_KEY)
                    extracted_data[selector.get('selector_id')] = single_data
                else:
                    extracted_data[selector.get('selector_id')] = elements_data
            else:
                _d = get_selector_element(self.response, selector)
                extracted_data[selector.get('selector_id')] = _d
        data[self.parser_name] = extracted_data
        return data
