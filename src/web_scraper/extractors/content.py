from .base import ExtractorBase
import json

class HTMLExtractor(ExtractorBase):

    def extract(self):
        return self.extract_fields(self.extractor_fields)


class MetaTagExtractor(ExtractorBase):


    def extract(self):
        # TODO - make this extractor with YAML later
        data = {}
        elements = self.get_elem_by_css(self.html, "meta")
        for element in elements:
            # for open graph type of meta tags
            meta_property = element.xpath("@{0}".format('property')).extract_first()
            meta_content = element.xpath("@{0}".format('content')).extract_first() 
            meta_name = element.xpath("@{0}".format('name')).extract_first()
            if meta_property:
                data[meta_property] = meta_content
            if meta_name:
                data[meta_name] = meta_content
        data =  dict(sorted(data.items(), key=lambda x: x[0]))
        data["title"] = self.get_value_by_css(self.html, 'title::text')
        return data


class TableContentExtractor(ExtractorBase):

    def extract(self):

        table_el  = self.get_elem_by_css(self.html, "table")
        table_data = []
        if table_el is None:
            return table_data
        table_headers = [th.extract() for th in table_el.css("thead tr th::text")]
        for row in table_el.css("tbody tr"):
            row_data = [td.extract() for td in row.css("td::text")]
            row_dict = dict(zip(table_headers, row_data))
            table_data.append(row_dict)
        return table_data
    

class JSONLDExtractor(ExtractorBase):

    def extract(self):
        extracted_data = []
        elements = self.html.xpath('//script[@type="application/ld+json"]/text()').extract()
        for element in elements:
            # for open graph type of meta tags
            try:
                element = element.strip()
                element = json.loads(element)
                extracted_data.append(element)
            except Exception as e:
                pass

        return extracted_data


class IconsExtractor(ExtractorBase):

    def extract(self):
        meta_data_dict = {}

        favicon = self.html.xpath('//link[@rel="shortcut icon"]').xpath("@href").get()
        if favicon:
            meta_data_dict['favicon'] = favicon

        elements = self.html.xpath('//link[@rel="icon" or @rel="apple-touch-icon-precomposed"]')
        for element in elements:
            # for open graph type of meta tags
            meta_property = element.xpath("@sizes").extract_first()
            if meta_property:
                meta_property = meta_property.replace(":", "__").replace(".", "__")
                meta_data_dict[meta_property] = element.xpath("@{0}".format('href')).extract_first()
        return meta_data_dict

