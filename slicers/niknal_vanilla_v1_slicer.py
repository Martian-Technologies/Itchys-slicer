import json
import numpy as np
import os
from encoders.niknal_vanilla_v1_encoder import *


class NiknalVanillaV1Slicer:
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
        encoder = NiknalVanillaV1Encoder()
        order = NiknalVanillaV1Slicer.findOrder(32, 32)
        prev_pos = (0, 0)
        for z in range(32):
            for pos in order:
                if voxels[z][pos[1]][pos[0]] == 2:  # support
                    dist = max(pos[0]-prev_pos[0], pos[1]-prev_pos[1])
                    for j in range((dist-1)//2):
                        encoder.addInstruction(
                            (pos[0], pos[1], z), 0, 2)  # move don't place
                    encoder.addInstruction(
                        (pos[0], pos[1], z), 0, 1)  # move and place
                    prev_pos = pos
            for pos in reversed(order):
                if voxels[z][pos[1]][pos[0]] == 1:  # model
                    dist = max(pos[0]-prev_pos[0], pos[1]-prev_pos[1])
                    for j in range((dist-1)//2):
                        encoder.addInstruction(
                            (pos[0], pos[1], z), 1, 2)  # move don't place
                    encoder.addInstruction((pos[0], pos[1], z), 1, 0)
                    prev_pos = pos
        encoder.addInstruction((31, 31, 31), 1, 3)
        return encoder.getInstructions()

    @staticmethod
    def findOrder(n, m):
        result = [0]*(n*m)
        result[0] = (0, 0)
        k = 1
        i = j = 0
        while (k < n*m):
            while i >= 1 and j < n-1:
                i -= 1
                j += 1
                result[k] = (i, j)
                k += 1
            if j < n-1:
                j += 1
                result[k] = (i, j)
                k += 1
            elif i < m-1:
                i += 1
                result[k] = (i, j)
                k += 1
            while i < m-1 and j >= 1:
                i += 1
                j -= 1
                result[k] = (i, j)
                k += 1
            if i < m-1:
                i += 1
                result[k] = (i, j)
                k += 1
            elif j < n-1:
                j += 1
                result[k] = (i, j)
                k += 1
        return result
