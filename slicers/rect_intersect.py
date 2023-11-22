import numpy as np


class RectIntersect:
    @staticmethod
    def flip_vals(grid, from_val, to_val):
        return [[to_val if grid[i][j] == from_val else (from_val if grid[i][j] == to_val else grid[i][j]) for j in range(len(grid[0]))] for i in range(len(grid))]

    @staticmethod
    def gridsub(grid1, grid2):
        return [[grid1[i][j] - grid2[i][j] for j in range(len(grid1[0]))] for i in range(len(grid1))]

    @staticmethod
    def gridadd(grid1, grid2):
        return [[grid1[i][j] + grid2[i][j] for j in range(len(grid1[0]))] for i in range(len(grid1))]

    @staticmethod
    def gridwrap(grid, value_options):
        return [[grid[i][j] % value_options for j in range(len(grid[0]))] for i in range(len(grid))]

    @staticmethod
    def printgrid(grid):
        for line in grid:
            print(' '.join(map(str, line)))

    @staticmethod
    def any_negs(grid):
        for line in grid:
            for item in line:
                if item < 0:
                    return True
        return False

    @staticmethod
    def grid_from_intersect(row, col):
        out = []
        for i in range(len(col)):
            out.append([])
            for j in range(len(row)):
                out[i].append(row[j] * col[i])
        return out

    @staticmethod
    def next_intersect_modif_step(grid_diff):
        rows = len(grid_diff)
        cols = len(grid_diff[0])
        row = [0] * cols
        col = [0] * rows
        new_row = [0] * cols
        new_col = [0] * rows
        inter_grid = RectIntersect.grid_from_intersect(row, col)
        for i in range(len(inter_grid)):
            for j in range(len(inter_grid[0])):
                if grid_diff[i][j] == 0:
                    continue
                new_row[j] = 1
                new_col[i] = 1
                if RectIntersect.any_negs(RectIntersect.gridsub(grid_diff, RectIntersect.grid_from_intersect(new_row, new_col))):
                    new_row = row.copy()
                    new_col = col.copy()
                    continue
                row = new_row.copy()
                col = new_col.copy()
        return row, col

    @staticmethod
    def all_zeros(grid):
        for line in grid:
            for item in line:
                if item != 0:
                    return False
        return True

    @staticmethod
    def calculate_absolute_delta_steps(grid_from, grid_to, value_options):
        steps = []
        diff = RectIntersect.gridwrap(
            RectIntersect.gridsub(grid_to, grid_from), value_options)
        while not RectIntersect.all_zeros(diff):
            row, col = RectIntersect.next_intersect_modif_step(diff)
            steps.append((row, col))
            diff = RectIntersect.gridsub(
                diff, RectIntersect.grid_from_intersect(row, col))
        return steps

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
        command_lines = []
        current_grid = self.flip_vals(
            [[0]*len(voxels[0][0])]*len(voxels[0]), 1, 2)
        for z in range(len(voxels)):
            print(z)
            grid = self.flip_vals(voxels[z], 1, 2)
            steps = RectIntersect.calculate_absolute_delta_steps(
                current_grid, grid, 4)
            for step in steps:
                cmd = list(step[0]) + list(step[1]) + [0, 0]
                command_lines.append(cmd)
            if len(steps) == 0:
                command_lines.append([0]*len(voxels[0][0])*2 + [0, 0])
            command_lines[-1][-2] = 1
            current_grid = grid
        command_lines[-1][-1] = 1
        return command_lines
