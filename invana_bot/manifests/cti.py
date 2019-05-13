import json
import sys
import os
import yaml


class CTIManifestManager(object):
    """



    """
    required_files = ["cti_manifest.json", "cti_transformations.py"]

    def __init__(self, cti_config_path=None):
        print("Setting ETI path as: {}".format(cti_config_path))
        self.cti_config_path = cti_config_path

    def import_files(self):
        print("self.cti_config_path", self.cti_config_path)
        self.cti_manifest = yaml.load(open("{}/cti_manifest.yml".format(self.cti_config_path)))
        sys.path.append(self.cti_config_path)
        """
        don't remove the import below, this will be the cti_transformations.py,
        which is one of the required file to run the job. This file will be provided by the 
        user during the run.
        """
        import cti_transformations
        self.cti_transformations_module = cti_transformations
        # print("cti_manifest is {}".format(self.cti_manifest))
        # print("cti_transformations_module is {}".format(self.cti_transformations_module))

    def validate_cti_path_and_files(self):
        errors = []

        try:
            files_in_path = os.listdir(self.cti_config_path)
        except Exception as e:
            errors.append("No such path exist {}".format(self.cti_config_path))
            files_in_path = []
        if errors == 0:
            for required_file in self.required_files:
                if required_file not in files_in_path:
                    errors.append("{} file not in the path {}".format(required_file, self.cti_config_path))
        return errors

    def import_cti_transformations(self):
        for transformation in self.cti_manifest.get("transformations", []):
            method_to_call = getattr(self.cti_transformations_module, transformation.get("transformation_fn"))
            transformation['transformation_fn'] = method_to_call

    def get_manifest(self):
        errors = self.validate_cti_path_and_files()
        if len(errors) > 0:
            return None, errors
        self.import_files()
        self.import_cti_transformations()
        return self.cti_manifest, errors
