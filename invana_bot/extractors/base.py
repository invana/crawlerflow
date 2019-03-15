class ExtractorBase(object):
    pass

    def __init__(self, response=None, extractor=None, parser_name=None):
        if None in [response, extractor, parser_name]:
            raise Exception("Invalid input to the extractor class, response, extractor and parser_name are mandatory")
        self.response = response
        self.extractor = extractor
        self.parser_name = parser_name
