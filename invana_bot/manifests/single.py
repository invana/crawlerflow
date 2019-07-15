import sys
import os
import yaml


class SingleCrawlerManifestManager(object):
    """



    """
    required_files = ["crawler_manifest.json", "crawler_manifest.py"]

    def __init__(self, config_path=None):
        print("Setting ETI path as: {}".format(config_path))
        self.config_path = config_path

    def import_files(self):
        # print("self.cti_config_path", self.config_path)
        self.current_crawler = yaml.load(open("{}/crawler_manifest.yml".format(self.config_path)))
        sys.path.append(self.config_path)
        import crawler_transformations
        self.cti_transformations_module = crawler_transformations
        # print("cti_manifest is {}".format(self.current_crawler))
        # print("cti_transformations_module is {}".format(self.cti_transformations_module))

    def validate_cti_path_and_files(self):
        errors = []

        try:
            files_in_path = os.listdir(self.config_path)
        except Exception as e:
            errors.append("No such path exist {}".format(self.config_path))
            files_in_path = []
        if errors == 0:
            for required_file in self.required_files:
                if required_file not in files_in_path:
                    errors.append("{} file not in the path {}".format(required_file, self.config_path))
        return errors

    def import_cti_transformations(self):
        for tranformation in self.current_crawler.get("transformations", []):
            method_to_call = getattr(self.cti_transformations_module, tranformation.get("transformation_fn"))
            tranformation['transformation_fn'] = method_to_call

    def get_manifest(self):
        errors = self.validate_cti_path_and_files()
        if len(errors) > 0:
            return None, errors
        self.import_files()
        self.import_cti_transformations()
        return self.current_crawler, errors
