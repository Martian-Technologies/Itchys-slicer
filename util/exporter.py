import json
import os
import numpy as np


class Exporter(object):
    def __init__(self, altpath=None, altfilename=None):
        self.path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Scrap Mechanic\\Data\\Importer\\" if altpath == None else altpath
        self.filename = "Importer.json" if altfilename == None else altfilename
    def startExport(self, allInstructionsArrays, altpath=None, altfilename=None):
        startpath = self.path
        startfilename = self.filename
        if altpath != None:
            self.path = altpath
        if altfilename != None:
            self.filename = altfilename
        # if allInstructionsArrays is one file
        if len(allInstructionsArrays.shape) == 1:
            print('path: ' + self.path)
            doExport = 'y' == input(f'export instructions into {self.filename} (y/n): ')
            if doExport:
                self.export(allInstructionsArrays, self.path, self.filename)
        self.path = startpath
        self.filename = startfilename

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