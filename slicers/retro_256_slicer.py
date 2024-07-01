import json
import numpy as np
import os
from encoders.multi_panel_command import *


class Retro256Slicer:
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
        encoder = MultiPanelCommand()
        order = Retro256Slicer.findOrder(256, 256)
        prev_pos = (0, 0)
        max_z = 0
        for z in range(voxels.shape[0]):
            print(z)
            for pos in order:
                if voxels[z][pos[1]][pos[0]] == 2:  # support
                    encoder.add_instruction(pos[0], pos[1], z, 7)  # move and place
            for pos in reversed(order):
                if voxels[z][pos[1]][pos[0]] == 1:  # model
                    encoder.add_instruction(pos[0], pos[1], z, 0)
                    max_z = z
        encoder.add_instruction(0, 0, max_z, -1)
        return encoder.get_instructions()

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
