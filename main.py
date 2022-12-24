from util.selector import *
from util.voxelizer import *
from util.exporter import *

from slicers.tower_slicer import *

path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Scrap Mechanic\\Data\\Importer\\"
filename = "Importer.json"

selector = Selector()
mesh = selector.select_3d_file()
print(type(mesh))
voxelizer = Voxelizer()
voxels, voxelPostions = voxelizer.fixVoxels(voxelizer.voxelize(mesh, 1))

slicer = TowerSlicer()
voxels, newvVoxelPositions = slicer.slice(voxels, voxelPostions)
allInstructionsArrays = slicer.cam(voxels)

exporter = Exporter()
exporter.startExport(allInstructionsArrays, filename, path)