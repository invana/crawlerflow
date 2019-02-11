class DefaultPipelineParser(object):
    db = None

    def __init__(self, config=None):
        self.config = config

    def find_pipe(self, pipe_id=None):
        pass

    def get_database(self):
        # TODO - get the connection details from pipeline
        # Note - returns self.db_client that can be used to save the data
        pass

    def get_database_details(self):
        pass

    @property
    def pipeline(self):
        return self.config['pipeline']

    def run_extractors(self, pipe_id=None):
        pass

    def run_traversals(self, pipe_id=None):
        pass

    def save(self):
        # TODO - saves to the self.db_client
        pass
