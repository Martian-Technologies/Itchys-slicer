import json
import os
import numpy as np


class Exporter:
    def __init__(self):
        self.path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Scrap Mechanic\\Data\\Importer\\"
        self.filename = "Importer.json"
    def startExport(self, allInstructionsArrays):

        # if allInstructionsArrays is one file
        if len(allInstructionsArrays.shape) == 1:
            print('path: ' + self.path)
            doExport = 'y' == input(f'export instructions into {self.filename} (y/n): ')
            if doExport:
                self.export(allInstructionsArrays, self.path, self.filename)

        # if allInstructionsArrays is two files
        else:
            print('path: ' + self.path)
            doExports = 'y' == input(f'export {len(allInstructionsArrays)} instructions (y/n): ')
            if doExports:
                for i in range(len(allInstructionsArrays)):
                    doExport = 'y' == input(f'export instructions {i+1}/{len(allInstructionsArrays)} into {self.filename} (y/n): ')
                    if doExport:
                        self.export(allInstructionsArrays[i])


    def export(self, data):
        print(data)
        # print(dict(data))
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        # for i in data:
        #     dataDict[string(i)]
        with open(self.path + self.filename, "w") as f:
            f.write(json.dumps(list(data)))