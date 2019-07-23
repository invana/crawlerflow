from invana_bot.extractors.base import ExtractorBase


class PythonBasedExtractor(ExtractorBase):
    """


    def extractor_fn(response=response):
        html_content = response.title

        return {"data": {}, "d__d": []}


    """

    def run(self):
        print("-======response", type(self.response), self.extractor)
        extractor_fn = self.extractor.get("extractor_fn")
        print ("extractor_fn=", extractor_fn)
        # exit()
        data = {}
        if extractor_fn:
            data[self.extractor_id] = extractor_fn(response=self.response)
        return data
