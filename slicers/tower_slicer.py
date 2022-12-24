import json
import numpy as np
import os
from encoders.legacy import *


class TowerSlicer:
    def slice(self, voxels, voxelPositions):
        newvVoxelPositions = voxelPositions.copy()
        for vox in voxelPositions:
            voxels, newvVoxelPositions = self.checkPosition(
                voxels, vox, newvVoxelPositions)
        return voxels, newvVoxelPositions

    def checkPosition(self, voxels, vox, newvVoxelPositions):
        if vox[2] > 0:
            vox = [vox[0], vox[1], vox[2]-1]
            if (voxels[vox[2]][vox[1]][vox[0]] == 0):
                voxels[vox[2]][vox[1]][vox[0]] = 2
                newvVoxelPositions = np.append(newvVoxelPositions, vox)
                voxels, newvVoxelPositions = self.checkPosition(
                    voxels, vox, newvVoxelPositions)
        return voxels, newvVoxelPositions

    def cam(self, voxels):
        numberOfHeads = int(input('how many print heads do you have: '))
        allInstructions = np.empty(0, dtype=Legacy)
        for i in range(numberOfHeads):
            allInstructions = np.append(allInstructions, Legacy())
        allInstructionsArrays_Cords = []
        headNumber = 0
        for z in range(len(voxels)):
            for y in range(len(voxels[z])):
                for x in range(len(voxels[z][y])):
                    allInstructionsArrays_Cords.append(
                        f"{x+2}, {y+2}, {z}, {voxels[z][y][x]}")
                    if voxels[z][y][x] == 1:
                        allInstructions[headNumber].addInstruction(
                            [x+2, y+2, z], 0, 256)
                    elif voxels[z][y][x] == 2:
                        allInstructions[headNumber].addInstruction(
                            [x+2, y+2, z], 1, 256)
                    headNumber = headNumber + 1
                    if headNumber >= len(allInstructions):
                        headNumber = 0

        allInstructionsArrays = None
        if len(allInstructions) > 1:
            allInstructionsArrays = []
            for i in range(len(allInstructions)):
                allInstructions[i].addInstruction([0, 0, 0], 3, 256)
                allInstructionsArrays.append(
                    allInstructions[i].getInstructions())
        else:
            allInstructions[0].addInstruction([0, 0, 0], 3, 256)
            allInstructionsArrays = allInstructions[0].getInstructions()

        return allInstructionsArrays
