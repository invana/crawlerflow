from .base import ExtractorBase


class HTMLExtractor(ExtractorBase):

    def extract(self):
        return self.extract_fields(self.extractor_fields)


class MetaExtractor(ExtractorBase):


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