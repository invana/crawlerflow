import json
import sys


class ETIManifestManager(object):
    """



    """

    def __init__(self, cti_config_path=None):
        print("cti_config_path is {}".format(cti_config_path))
        self.cti_manifest = json.load(open("{}/eti_manifest.json".format(cti_config_path)))
        sys.path.append(cti_config_path)
        import eti_transformations
        self.eti_transformations_module = eti_transformations
        print("cti_manifest is {}".format(self.cti_manifest))
        print("eti_transformations_module is {}".format(self.eti_transformations_module))

    def import_eti_transformations(self):
        for tranformation in self.cti_manifest.get("transformations", []):
            method_to_call = getattr(self.eti_transformations_module, tranformation.get("transformation_fn"))
            tranformation['transformation_fn'] = method_to_call

    def get_manifest(self):
        self.import_eti_transformations()
        return self.cti_manifest
