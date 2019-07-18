import sys
import os
import yaml


class CTIManifestManager(object):
    """



    """
    ib_functions = None
    required_files = ["manifest.yml", "ib_functions.py"]
    manifest = None

    def __init__(self, manifest_path=None):
        print("Setting ETI path as: {}".format(manifest_path))
        self.manifest_path = manifest_path

    def import_files(self):
        print("self.manifest_path", self.manifest_path)
        self.manifest = yaml.load(open("{}/manifest.yml".format(self.manifest_path)), Loader=yaml.FullLoader)
        sys.path.append(self.manifest_path)
        """
        don't remove the import below, this will be the cti_transformations.py,
        which is one of the required file to run the job. This file will be provided by the 
        user during the run.
        """
        try:
            import ib_functions
        except Exception as e:
            ib_functions = None
        self.ib_functions = ib_functions
        print ("self.ib_functions is {}".format(ib_functions))
        # print("manifest is {}".format(self.manifest))
        # print("ib_functions is {}".format(self.ib_functions))

    def validate_cti_path_and_files(self):
        errors = []

        try:
            files_in_path = os.listdir(self.manifest_path)
        except Exception as e:
            errors.append("No such path exist {}".format(self.manifest_path))
            files_in_path = []
        if errors == 0:
            for required_file in self.required_files:
                if required_file not in files_in_path:
                    errors.append("{} file not in the path {}".format(required_file, self.manifest_path))
        return errors

    def import_cti_transformations(self):
        if self.ib_functions:
            for transformation in self.manifest.get("transformations", []):
                method_to_call = getattr(self.ib_functions, transformation.get("transformation_fn"))
                transformation['transformation_fn'] = method_to_call

    def import_extractor_functions(self):
        if self.ib_functions:
            for spider in self.manifest.get("spiders", []):
                for extractor in spider.get("extractors", []):
                    method_to_call = getattr(self.ib_functions, extractor.get("extractor_fn"))
                    extractor['extractor_fn'] = method_to_call

    def get_manifest(self):
        errors = self.validate_cti_path_and_files()
        if len(errors) > 0:
            return None, errors
        self.import_files()
        self.import_cti_transformations()
        self.import_extractor_functions()
        print ("=====+++++++++============")
        return self.manifest, errors
