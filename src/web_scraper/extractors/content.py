from .base import ExtractorBase


class HTMLExtractor(ExtractorBase):

    def extract(self):
        return self.extract_fields(self.extractor_fields)


class MetaExtractor(ExtractorBase):
    def extract(self):
        # TODO - make this extractor with YAML later
        data = {}

        elements = self.html.css('meta')
        for element in elements:
            # for open graph type of meta tags
            meta_property = element.xpath("@{0}".format('property')).extract_first()
            if meta_property:
                meta_property = meta_property.replace(":", "__").replace(".", "__")
                data[meta_property] = element.xpath(
                    "@{0}".format('content')).extract_first() or element.xpath("@{0}".format('value')).extract_first()

            meta_name = element.xpath("@{0}".format('name')).extract_first()
            if meta_name:
                meta_name = meta_name.replace(":", "__").replace(".", "__")
                data["meta__{}".format(meta_name)] = element.xpath(
                    "@{0}".format('content')).extract_first() or element.xpath("@{0}".format('value')).extract_first()

        try:
            title = self.html.css('title::text').get()
            if title:
                data["title"] = title
        except Exception as e:
            pass
        return data