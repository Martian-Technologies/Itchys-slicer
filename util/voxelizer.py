import numpy as np
import trimesh
from trimesh.voxel.creation import voxelize


class Voxelizer:
    def __init__(self) -> None:
        pass

    def voxelize(self, mesh, pitch, invert_yz=False):
        if invert_yz:
            mesh_copy = mesh.copy()
            verts = mesh_copy.vertices
            new_verts = verts.copy()
            new_verts[:, 1] = verts[:, 2]
            new_verts[:, 2] = verts[:, 1]
            mesh_copy.vertices = new_verts
            return voxelize(mesh_copy, pitch)
        else:
            return voxelize(mesh, pitch)

    def fixVoxels(self, voxels):
        voxels.show()
        v_shape = voxels.shape
        voxels = voxels.points_to_indices(voxels.points)

        voxelPostions = np.empty([len(voxels), 3], dtype=int)
        for i in range(len(voxels)):
            voxelPostions[i] = [voxels[i][0], voxels[i][2], voxels[i][1] + 1]

        voxels = np.zeros([v_shape[1]+1, v_shape[2], v_shape[0]])
        for i in range(len(voxelPostions)):
            vox = voxelPostions[i]
            voxels[vox[2]][vox[1]][vox[0]] = 1

        return voxels, voxelPostions
    
    def move_to_center(self, voxels, voxelPostions, build_plate):
        # print(voxels)

        new_voxels = np.zeros([voxels.shape[0], build_plate[1], build_plate[0]])
        x_offset = int((build_plate[0] - voxels.shape[2]) / 2)
        y_offset = int((build_plate[1] - voxels.shape[1]) / 2)
        voxelPostions[:, 0] += x_offset
        voxelPostions[:, 1] += y_offset
        for pos in voxelPostions:
            new_voxels[pos[2]][pos[1]][pos[0]] = 1

        # print(new_voxels)

        return new_voxels, voxelPostions