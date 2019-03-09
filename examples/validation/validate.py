from invana_bot.utils.config import InvanaBotConfigValidator

import json

cti_manifest = json.load(open("../eti_full.json"))

validator = InvanaBotConfigValidator(config=cti_manifest)
validator.validate()