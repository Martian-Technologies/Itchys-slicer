import numpy as np
from encoders.legacy import *


class TowerSlicer:
    def slice(self, voxels, voxelPostions):
        newvVoxelPostions = voxelPostions.copy()
        for vox in voxelPostions:
            voxels, newvVoxelPostions = self.checkPostion(voxels, vox, newvVoxelPostions)
        return voxels, newvVoxelPostions


    def checkPostion(self, voxels, vox, newvVoxelPostions):
        if vox[2] > 0:
            print(vox)
            vox = [vox[0], vox[1], vox[2]-1]
            if(voxels[vox[2]][vox[1]][vox[0]] == 0):
                voxels[vox[2]][vox[1]][vox[0]] = 2
                newvVoxelPostions = np.append(newvVoxelPostions, vox)
                voxels, newvVoxelPostions = self.checkPostion(voxels, vox, newvVoxelPostions)
        return voxels, newvVoxelPostions

    
    def cam(self, voxels):
        print(voxels)
        numberOfHeads = int(input('how many print heads do you have: '))
        allInstructions = np.empty(0, dtype=Legacy)
        for i in range(numberOfHeads):
            allInstructions = np.append(allInstructions, Legacy())

        headNumber = 0
        for z in range(len(voxels) - 1):
            for y in range(len(voxels[z]) - 1):
                for x in range(len(voxels[z][y]) - 1):
                    if voxels[z][y][x] == 1:
                        allInstructions[headNumber].addInstruction([x, y, z], 0, 256)
                    elif voxels[z][y][x] == 2:
                        allInstructions[headNumber].addInstruction([x, y, z], 1, 256)
                    headNumber = headNumber + 1
                    if headNumber > len(allInstructions)-1:
                        headNumber = 0

        allInstructionsArrays = np.empty(0, dtype=np.ndarray)
        print("foo")
        for i in range(len(allInstructions) - 1):
            print(i)
            allInstructions[i].addInstruction([0, 0, 0], 4, 256)
            allInstructionsArrays = np.append(allInstructionsArrays, allInstructions[i].getInstructions())

        return allInstructionsArrays
