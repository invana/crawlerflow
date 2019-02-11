class DefaultPipelineParser(object):
    db = None

    def __init__(self, config=None):
        self.config = config

    def find_pipe(self, pipe_id=None):
        pass

    def get_db(self):
        # TODO - get the connection details from pipeline
        # Note - self.db
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
        # TODO - saves to the self.db
        pass
