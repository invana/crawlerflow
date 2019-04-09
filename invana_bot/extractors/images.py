from invana_bot.extractors.base import ExtractorBase


class ImageExtractor(ExtractorBase):
    def run(self):
        data = {}
        images_data = self.response.css("img::src").extract()
        data[self.parser_name] = images_data
        return data
