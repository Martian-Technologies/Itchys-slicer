from util.selector import *
from util.voxelizer import *
from util.exporter import *

from slicers.tower_slicer import *

selector = Selector()
mesh = selector.select_3d_file()

voxelizer = Voxelizer()
voxels, voxelPostions = voxelizer.fixVoxels(voxelizer.voxelize(mesh, 1))

slicer = TowerSlicer()
voxels, voxelPostions = slicer.slice(voxels, voxelPostions)
allInstructionsArrays = slicer.cam(voxels)

exporter = Exporter()
exporter.startExport(allInstructionsArrays)