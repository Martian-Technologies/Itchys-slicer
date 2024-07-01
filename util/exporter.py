import json
import os
import numpy as np


class Exporter:

    def startExport(self, allInstructionsArrays, path):
        """starts the process of exporting to SM"""
        # if allInstructionsArrays is one file
        doExport = 'y' == input(
            f'export instructions into {path} (y/n): ')
        if doExport:
            self.export(allInstructionsArrays, path)

        # if type(allInstructionsArrays[0]) != list:
        #     print('path: ' + path)
        #     doExport = 'y' == input(
        #         f'export instructions into {filename} (y/n): ')
        #     if doExport:
        #         self.export(allInstructionsArrays, path, filename)

        # # if allInstructionsArrays is more than one file
        # else:
        #     print('path: ' + path)
        #     doExports = 'y' == input(
        #         f'export {len(allInstructionsArrays)} instructions (y/n): ')
        #     if doExports:
        #         for i in range(len(allInstructionsArrays)):
        #             doExport = 'y' == input(
        #                 f'export instructions {i+1}/{len(allInstructionsArrays)} into {filename} (y/n): ')
        #             if doExport:
        #                 self.export(allInstructionsArrays[i], path, filename)

    def export(self, data, path):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path, "w") as f:
            f.write(json.dumps(list(data)))
