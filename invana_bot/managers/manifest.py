import json
import sys
import os


class ETIManifestManager(object):
    """



    """
    required_files = ["eti_manifest.json", "eti_transformations.py"]

    def __init__(self, cti_config_path=None):
        print("Setting ETI path as: {}".format(cti_config_path))
        self.cti_config_path = cti_config_path

    def import_files(self):
        print ("self.cti_config_path", self.cti_config_path)
        self.cti_manifest = json.load(open("{}/eti_manifest.json".format(self.cti_config_path)))
        sys.path.append(self.cti_config_path)
        import eti_transformations
        self.eti_transformations_module = eti_transformations
        print("cti_manifest is {}".format(self.cti_manifest))
        print("eti_transformations_module is {}".format(self.eti_transformations_module))

    def validate_eti_path_and_files(self):
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

    def import_eti_transformations(self):
        for tranformation in self.cti_manifest.get("transformations", []):
            method_to_call = getattr(self.eti_transformations_module, tranformation.get("transformation_fn"))
            tranformation['transformation_fn'] = method_to_call

    def get_manifest(self):
        errors = self.validate_eti_path_and_files()
        if len(errors) > 0:
            return None, errors
        self.import_files()
        self.import_eti_transformations()
        return self.cti_manifest, errors
