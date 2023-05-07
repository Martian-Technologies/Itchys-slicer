import numpy as np

class Gigachad:
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
        commands = []
        for z in range(len(voxels)):
            y = 0
            x = -3
            x_dir = 1
            while y < len(voxels[z]):
                while (x < len(voxels[z][y]) if x_dir == 1 else x > -3):
                    p0 = False
                    p1 = False
                    if x >= 0:
                        if voxels[z][y][x] == 1:
                            p0 = True
                    if x < len(voxels[z][y])-3:
                        if voxels[z][y][x+3] == 2:
                            p1 = True
                    if p0 or p1:
                        commands.extend([y+4, z, 63-x])
                        commands.extend([1 if p0 else 0, 1 if p1 else 0, 0])
                    x += x_dir
                x_dir *= -1
                x += x_dir
                y += 1
        commands.extend([0, len(voxels)+4, 0, 0, 0, 0])
        commands.extend([0, 0, 0, 0, 0, 1])
        print(len(commands))
        return commands