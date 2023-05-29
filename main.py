from util.selector import *
from util.voxelizer import *
from util.exporter import *
from util.vanilla_exporter import *
from slicers.tower_slicer import *
from slicers.cartesian_additive import *
from slicers.gigachad import *
from slicers.rect_intersect import *


# path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Scrap Mechanic\\Data\\Importer\\"
# filename = "Importer.json"

# gets the 3d file
selector = Selector()
mesh = selector.select_3d_file(file='3D_models/duck.stl')

# Voxelizes the 3d file
voxelizer = Voxelizer()
voxels, voxelPostions = voxelizer.fixVoxels(
    voxelizer.voxelize(mesh, invert_yz=True, max_y=16))
voxels, voxelPostions = voxelizer.move_to_center(
    voxels, voxelPostions, (32, 32))

# print(voxels[1])
# uses a slicer to slice/cam the 3d file
slicer = RectIntersect()
voxels, newvVoxelPositions = slicer.slice(voxels, voxelPostions)
allInstructionsArrays = slicer.cam(voxels)

# exports the intructions to path, filename
exporter = VanillaExporter()
exporter.startExport(allInstructionsArrays, '.\\', 'duck.json')
