import numpy as np
from encoders.single_number import *
import random

class Cartesian(object):
    def __init__(self, option2):
        if option2 not in ['none', 'line', 'rect']:
            raise Exception('Invalid option2, must be one of: none, line, rect. Received {}'.format(option2))
        self.option2 = option2
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
        print_head_x = 0
        print_head_y = 0
        for z, layer_og in enumerate(voxels):
            layer = layer_og.copy()
            print('-'*100)
            print(layer)
            rectangles = []
            while np.sum(layer) > 0:
                pos = (random.randint(0, len(layer[0])-1), random.randint(0, len(layer)-1))
                while layer[pos[1]][pos[0]] == 0:
                    pos = (random.randint(0, len(layer[0])-1), random.randint(0, len(layer)-1))
                rect = [layer[pos[1]][pos[0]], pos[0], pos[1], pos[0], pos[1]]
                pos_x_fail = False
                pos_y_fail = False
                neg_x_fail = False
                neg_y_fail = False
                while not pos_x_fail or not pos_y_fail or not neg_x_fail or not neg_y_fail:
                    for y in range(rect[2], rect[4]+1):
                        if pos_x_fail:
                            break
                        if rect[3] >= len(layer[0])-1:
                            pos_x_fail = True
                            break
                        if layer[y][rect[3]+1] != rect[0]:
                            pos_x_fail = True
                            break
                    if not pos_x_fail:
                        rect[3] += 1
                    for y in range(rect[2], rect[4]+1):
                        if neg_x_fail:
                            break
                        if rect[1] <= 0:
                            neg_x_fail = True
                            break
                        if layer[y][rect[1]-1] != rect[0]:
                            neg_x_fail = True
                            break
                    if not neg_x_fail:
                        rect[1] -= 1
                    for x in range(rect[1], rect[3]+1):
                        if pos_y_fail:
                            break
                        if rect[4] >= len(layer)-1:
                            pos_y_fail = True
                            break
                        if layer[rect[4]+1][x] != rect[0]:
                            pos_y_fail = True
                            break
                    if not pos_y_fail:
                        rect[4] += 1
                    for x in range(rect[1], rect[3]+1):
                        if neg_y_fail:
                            break
                        if rect[2] <= 0:
                            neg_y_fail = True
                            break
                        if layer[rect[2]-1][x] != rect[0]:
                            neg_y_fail = True
                            break
                    if not neg_y_fail:
                        rect[2] -= 1
                for y in range(rect[2], rect[4]+1):
                    for x in range(rect[1], rect[3]+1):
                        layer[y][x] = 0
                rectangles.append(rect)
                # print(rect)
            for rect in rectangles:
                print(rect)
            passthroughs = []
            for rect in rectangles:
                if rect[0] == 2:
                    portals = []
                    x_width = rect[3]-rect[1]
                    y_width = rect[4]-rect[2]
                    if x_width >= y_width:
                        major = 'x'
                        major_width = x_width
                        minor_width = y_width
                    else:
                        major = 'y'
                        major_width = y_width
                        minor_width = x_width
                    if major == 'x':
                        portals.append({
                            'x1': rect[1],
                            'y1': rect[2],
                            'x2': rect[1] if minor_width%2==0 else rect[3],
                            'y2': rect[4]
                        })
                        portals.append({
                            'x1': rect[3],
                            'y1': rect[2],
                            'x2': rect[3] if minor_width%2==0 else rect[1],
                            'y2': rect[4]
                        })
                    else:
                        portals.append({
                            'x1': rect[1],
                            'y1': rect[2],
                            'x2': rect[3],
                            'y2': rect[2] if minor_width%2==0 else rect[4]
                        })
                        portals.append({
                            'x1': rect[1],
                            'y1': rect[4],
                            'x2': rect[3],
                            'y2': rect[4] if minor_width%2==0 else rect[2]
                        })
                    passthroughs.append({
                        'block': 2,
                        'x1': rect[1],
                        'y1': rect[2],
                        'x2': rect[3],
                        'y2': rect[4],
                        'major': major,
                        'portals': portals
                    })
            best_time = self.calculate_deadtime(passthroughs, print_head_x, print_head_y)
            best_pass = passthroughs.copy()
            for i in range(1000):
                random.shuffle(passthroughs)
                time = self.calculate_deadtime(passthroughs, print_head_x, print_head_y)
                if time < best_time:
                    best_time = time
                    best_pass = passthroughs.copy()
            for passthrough in best_pass:
                print(passthrough)
            input()
    def calculate_deadtime(self, passthroughs, current_head_x, current_head_y):
        deadtime = []
        pos_x = current_head_x
        pos_y = current_head_y
        for passthrough in passthroughs:
            shortest_travel = None
            for portal in passthrough['portals']:
                travel = max(abs(portal['x1']-pos_x), abs(portal['y1']-pos_y))
                if shortest_travel is None or travel < shortest_travel[0]:
                    shortest_travel = (travel, (portal['x2'], portal['y2']))
                travel = max(abs(portal['x2']-pos_x), abs(portal['y2']-pos_y))
                if shortest_travel is None or travel < shortest_travel[0]:
                    shortest_travel = (travel, (portal['x1'], portal['y1']))
            deadtime.append(shortest_travel[0])
            pos_x = shortest_travel[1][0]
            pos_y = shortest_travel[1][1]
        return sum(deadtime)