class ExtractorBase(object):
    pass

    def __init__(self, response=None, extractor=None, parser_id=None):
        if None in [response, extractor, parser_id]:
            raise Exception("Invalid input to the extractor class, response, extractor and parser_id are mandatory")
        self.response = response
        self.extractor = extractor
        self.parser_id = parser_id
