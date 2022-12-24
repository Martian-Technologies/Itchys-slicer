import json
import os
import numpy as np


class Exporter:
    def startExport(self, allInstructionsArrays):
        path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Scrap Mechanic\\Data\\Importer\\"
        filename = "Importer.json"

        # if allInstructionsArrays is one file
        if len(allInstructionsArrays.shape) == 1:
            print('path: ' + path)
            doExport = 'y' == input(f'export instructions into {filename} (y/n): ')
            if doExport:
                self.export(allInstructionsArrays, path, filename)

        # if allInstructionsArrays is two files
        else:
            print('path: ' + path)
            doExports = 'y' == input(f'export {len(allInstructionsArrays)} instructions (y/n): ')
            if doExports:
                for i in range(len(allInstructionsArrays)):
                    doExport = 'y' == input(f'export instructions {i+1}/{len(allInstructionsArrays)} into {filename} (y/n): ')
                    if doExport:
                        self.export(allInstructionsArrays[i], path, filename)


    def export(self, data, path, filename):
        print(data)
        print(dict(data))
        if not os.path.exists(path):
            os.makedirs(path)
        for i in data:
            dataDict[string(i)]
        with open(path + filename, "w") as f:
            f.write(json.dumps(dict(data)))