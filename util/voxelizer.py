import numpy as np
import trimesh
from trimesh.voxel.creation import voxelize


class Voxelizer:
    def __init__(self) -> None:
        pass

    def voxelize(self, mesh, pitch):
        return voxelize(mesh, pitch)
        
    def fixVoxels(self, voxels):
        voxels.show()
        v_shape = voxels.shape
        voxels = voxels.points_to_indices(voxels.points)

        voxelPostions = np.empty([len(voxels),3], dtype=int)
        for i in range(len(voxels)):
            voxelPostions[i] = [voxels[i][0], voxels[i][2], voxels[i][1] + 1]

        voxels = np.zeros([v_shape[1]+1, v_shape[2], v_shape[0]])
        for i in range(len(voxelPostions)):
            vox = voxelPostions[i]
            voxels[vox[2]][vox[1]][vox[0]] = 1
        return voxels, voxelPostions
    
