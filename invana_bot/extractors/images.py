from invana_bot.extractors.base import ExtractorBase


class ImageExtractor(ExtractorBase):
    def run(self):
        data = {}
        images_data = []
        images_selector = self.response.css("img")
        for selector in images_selector:
            images_data.append(selector.get("src"))
        data[self.parser_id] = images_data
        return data
