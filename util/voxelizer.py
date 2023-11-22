import numpy as np
import trimesh
from trimesh.voxel.creation import voxelize


class Voxelizer:
    def __init__(self) -> None:
        pass

    def voxelize(self, mesh, pitch=None, max_x=None, max_y=None, max_z=None, invert_yz=False):
        max_pitch = pitch if pitch is not None else 0
        if invert_yz:
            max_y, max_z = max_z, max_y
        if max_x is not None:
            # get x_size of mesh
            x_size = mesh.bounds[1][0] - mesh.bounds[0][0]
            # get max pitch
            max_pitch = max(max_pitch, x_size / max_x)
        if max_y is not None:
            # get y_size of mesh
            y_size = mesh.bounds[1][1] - mesh.bounds[0][1]
            # get max pitch
            max_pitch = max(max_pitch, y_size / max_y)
        if max_z is not None:
            # get z_size of mesh
            z_size = mesh.bounds[1][2] - mesh.bounds[0][2]
            # get max pitch
            max_pitch = max(max_pitch, z_size / max_z)
        print(max_pitch)
        if max_pitch == 0:
            max_pitch = 1
        if invert_yz:
            mesh_copy = mesh.copy()
            verts = mesh_copy.vertices
            new_verts = verts.copy()
            new_verts[:, 1] = verts[:, 2]
            new_verts[:, 2] = verts[:, 1]
            mesh_copy.vertices = new_verts
            return voxelize(mesh_copy, max_pitch)
        else:
            return voxelize(mesh, max_pitch)

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

        new_voxels = np.zeros(
            [voxels.shape[0], build_plate[1], build_plate[0]])
        x_offset = int((build_plate[0] - voxels.shape[2]) / 2)
        y_offset = int((build_plate[1] - voxels.shape[1]) / 2)
        voxelPostions[:, 0] += x_offset
        voxelPostions[:, 1] += y_offset
        for pos in voxelPostions:
            new_voxels[pos[2]][pos[1]][pos[0]] = 1

        # print(new_voxels)

        return new_voxels, voxelPostions
