from invana_bot.extractors.base import ExtractorBase
from invana_bot.utils.selectors import get_selector_element
from invana_bot.utils.url import get_urn, get_domain
import json


class ParagraphsExtractor(ExtractorBase):
    def run(self):
        data = {}
        extracted_data = []
        elements = self.response.css("p::text").extract()
        for el in elements:
            extracted_data.append(el)
        data[self.extractor_id] = [d.strip() for d in extracted_data]
        return data


class HeadingsExtractor(ExtractorBase):
    # TODO - implement this
    def run(self):
        data = {}
        extracted_data = []
        heading_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]
        elements = self.response.css(",".join(heading_tags)).extract()
        for el in elements:
            extracted_data.append(el)
        data[self.extractor_id] = [d.strip() for d in extracted_data]
        return data


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
        data[self.extractor_id] = tables
        return data


class MetaTagExtractor(ExtractorBase):
    def run(self):
        data = {}
        meta_data_dict = {}

        elements = self.response.css('meta')
        for element in elements:
            # for open graph type of meta tags
            meta_property = element.xpath("@{0}".format('property')).extract_first()
            if meta_property:
                meta_property = meta_property.replace(":", "__").replace(".", "__")
                meta_data_dict[meta_property] = element.xpath(
                    "@{0}".format('content')).extract_first() or element.xpath("@{0}".format('value')).extract_first()

            meta_name = element.xpath("@{0}".format('name')).extract_first()
            if meta_name:
                meta_name = meta_name.replace(":", "__").replace(".", "__")
                meta_data_dict["meta__{}".format(meta_name)] = element.xpath(
                    "@{0}".format('content')).extract_first() or element.xpath("@{0}".format('value')).extract_first()

        try:
            title = self.response.css('title::text').get()
            if title:
                meta_data_dict["title"] = title
        except Exception as e:
            pass
        data[self.extractor_id] = meta_data_dict
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
        data[self.extractor_id] = extracted_data
        return data


class IconsExtractor(ExtractorBase):
    def run(self):
        data = {}
        meta_data_dict = {}

        favicon = self.response.xpath('//link[@rel="shortcut icon"]').xpath("@href").get()
        if favicon:
            meta_data_dict['favicon'] = favicon

        elements = self.response.xpath('//link[@rel="icon" or @rel="apple-touch-icon-precomposed"]')
        for element in elements:
            # for open graph type of meta tags
            meta_property = element.xpath("@sizes").extract_first()
            if meta_property:
                meta_property = meta_property.replace(":", "__").replace(".", "__")
                meta_data_dict[meta_property] = element.xpath("@{0}".format('href')).extract_first()
        data[self.extractor_id] = meta_data_dict
        return data


class JSONLDExtractor(ExtractorBase):

    def run(self):
        data = {}
        extracted_data = []

        elements = self.response.xpath('//script[@type="application/ld+json"]/text()').extract()
        for element in elements:
            # for open graph type of meta tags
            try:
                element = element.strip()
                element = json.loads(element)
                extracted_data.append(element)
            except Exception as e:
                pass

        data[self.extractor_id] = extracted_data
        return data


class PlainHTMLContentExtractor(ExtractorBase):

    def run(self):
        data = {}
        response_text = self.response.body
        data[self.extractor_id] = response_text
        return data


class FeedUrlExtractor(ExtractorBase):
    def run(self):
        data = {}
        data[self.extractor_id] = {}
        data[self.extractor_id]['rss__xml'] = self.response.xpath('//link[@type="application/rss+xml"]').xpath(
            "@href").extract_first()
        data[self.extractor_id]['rss__atom'] = self.response.xpath('//link[@type="application/atom+xml"]').xpath(
            "@href").extract_first()
        return data


class PageOverviewExtractor(ExtractorBase):

    def run(self):
        data = {}

        meta_tags_data = MetaTagExtractor(
            response=self.response,
            extractor=self.extractor,
            extractor_id=self.extractor_id
        ).run().get(self.extractor_id, {})

        paragraphs_data = ParagraphsExtractor(
            response=self.response,
            extractor=self.extractor,
            extractor_id="paragraphs"
        ).run().get("paragraphs", {})
        # TODO - clean the data, that is extracted. ex:  meta_tags_data.get("title")
        extracted_data = {
            "title":
                meta_tags_data.get("title") or
                meta_tags_data.get("meta__title") or
                meta_tags_data.get("og__title") or
                meta_tags_data.get("fb__title") or
                meta_tags_data.get("meta__twitter__title"),
            "description":
                meta_tags_data.get("description") or
                meta_tags_data.get("meta__description") or
                meta_tags_data.get("og__description") or
                meta_tags_data.get("fb__description") or
                meta_tags_data.get("meta__twitter__description"),
            "image":
                meta_tags_data.get("image") or
                meta_tags_data.get("meta__image") or
                meta_tags_data.get("og__image") or
                meta_tags_data.get("fb__image") or
                meta_tags_data.get("meta__twitter__image"),
            "url":
                meta_tags_data.get("url") or
                meta_tags_data.get("meta__url") or
                meta_tags_data.get("og__url") or
                meta_tags_data.get("fb__url") or
                meta_tags_data.get("meta__twitter__url"),
            "page_type": meta_tags_data.get("og__type"),
            "keywords": meta_tags_data.get("meta__keywords"),
            "domain": get_domain(self.response.url),
            "first_paragraph": paragraphs_data[0] if len(paragraphs_data) > 0 else None,
            "shortlink_url": self.response.xpath('//link[@rel="shortlink"]').xpath("@href").extract_first(),
            "canonical_url": self.response.xpath('//link[@rel="canonical"]').xpath("@href").extract_first()
        }
        data[self.extractor_id] = extracted_data
        return data
