import json


class ETIManifestManager(object):
    """



    """
    CTI_CONFIG_PATH = "./basic"

    def __init__(self, cti_config_path=None, eti_transformations_module=None):
        self.cti_manifest = json.load(open("{}/eti_manifest.json".format(cti_config_path)))
        self.eti_transformations_module = eti_transformations_module
        print("cti_manifest is {}".format(self.cti_manifest))
        print("eti_transformations_module is {}".format(self.eti_transformations_module))

    def import_eti_transformations(self):
        for tranformation in self.cti_manifest.get("transformations", []):
            method_to_call = getattr(self.eti_transformations_module, tranformation.get("transformation_fn"))
            tranformation['transformation_fn'] = method_to_call
            print ("method_to_call", method_to_call)

    def get_manifest(self):
        self.import_eti_transformations()
        print ("cti_manifest", self.cti_manifest)
        return self.cti_manifest
