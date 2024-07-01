from util.selector import *
from util.voxelizer import *
from util.exporter import *
from util.vanilla_exporter import *
from slicers.tower_slicer import *
from slicers.cartesian_additive import *
from slicers.gigachad import *
from slicers.rect_intersect import *
from slicers.niknal_vanilla_v1_slicer import *
from slicers.retro_256_slicer import *


# path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Scrap Mechanic\\Data\\Importer\\"
# filename = "Importer.json"

# gets the 3d file
selector = Selector()
mesh = selector.select_3d_file() #file='3D_models/Amogus.stl'

# Voxelizes the 3d file
voxelizer = Voxelizer()
voxels, voxelPostions = voxelizer.fixVoxels(
    voxelizer.voxelize(mesh, invert_yz=True, max_y=32))
voxels, voxelPostions = voxelizer.move_to_center(
    voxels, voxelPostions, (256, 256))

# print(voxels[1])
# uses a slicer to slice/cam the 3d file
slicer = Retro256Slicer()
voxels, newvVoxelPositions = slicer.slice(voxels, voxelPostions)
allInstructionsArrays = slicer.cam(voxels)

# exports the intructions to path, filename
exporter = Exporter()
# exporter.startExport(allInstructionsArrays, '.\\', 'vanilla_tt.json')

import pathlib

# C:\Program Files (x86)\Steam\steamapps\common\Scrap Mechanic\Data\Importer
DEFAULT_PATH = pathlib.Path("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Scrap Mechanic\\Data\\Importer\\Importer.json")
import os

if os.path.exists('path.txt'):
    with open('path.txt', 'r') as f:
        path = f.read()
else:
    path = DEFAULT_PATH
    with open('path.txt', 'w') as f:
        f.write(str(path))

exporter.startExport(allInstructionsArrays, path)
