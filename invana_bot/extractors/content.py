from invana_bot.extractors.base import ExtractorBase
from invana_bot.utils.selectors import get_selector_element


class ParagraphsExtractor(ExtractorBase):
    def run(self):
        data = {}
        paragraphs_data = []
        elements = self.response.css("p").extract()
        for el in elements:
            paragraphs_data.append(el)
        data[self.parser_id] = paragraphs_data
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
        data[self.parser_id] = tables
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

        data[self.parser_id] = meta_data_dict
        return data


class CustomContentExtractor(ExtractorBase):

    def run(self):
        data = {}
        extracted_data = {}
        for selector in self.extractor.get('data_selectors', []):
            if selector.get('selector_attribute') == 'element' and len(selector.get('child_selectors', [])) > 0:
                # TODO - currently only support multiple elements strategy. what if multiple=False
                elements = self.response.css(selector.get('selector'))
                elements_data = []
                for el in elements:
                    datum = {}
                    for child_selector in selector.get('child_selectors', []):
                        _d = get_selector_element(el, child_selector)
                        datum[child_selector.get('selector_id')] = _d if _d else None
                    elements_data.append(datum)
                data_type = selector.get("data_type", "RawField")
                if data_type.startswith("List") is False:
                    single_data = elements_data[0]
                    extracted_data[selector.get('selector_id')] = single_data
                else:
                    extracted_data[selector.get('selector_id')] = elements_data
            else:
                _d = get_selector_element(self.response, selector)
                extracted_data[selector.get('selector_id')] = _d
        data[self.parser_id] = extracted_data
        return data
