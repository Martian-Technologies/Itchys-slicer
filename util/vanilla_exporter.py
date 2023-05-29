import json


class VanillaExporter:
    def startExport(self, allInstructionsArrays, path, filename):
        with open(path + filename, "w") as f:
            json.dump(list(allInstructionsArrays), f)
