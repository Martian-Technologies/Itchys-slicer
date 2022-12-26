import numpy as np
from encoders.multi_number_command import *
import random


class Cartesian(object):
    def __init__(self, option2, block=0, support=1):
        self.block = block
        self.support = support
        if option2 not in ['none', 'line', 'rect']:
            raise Exception(
                'Invalid option2, must be one of: none, line, rect. Received {}'.format(option2))

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
        exp = MultiNumberCommand()
        print_head_x = 0
        print_head_y = 0
        for z, layer_og in enumerate(voxels):
            layer = layer_og.copy()
            print('-'*100)
            print(layer)
            rectangles = []
            while np.sum(layer) > 0:
                pos = (random.randint(
                    0, len(layer[0])-1), random.randint(0, len(layer)-1))
                while layer[pos[1]][pos[0]] == 0:
                    pos = (random.randint(
                        0, len(layer[0])-1), random.randint(0, len(layer)-1))

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

            head = self.encode(2, rectangles, exp,
                               print_head_x, print_head_y, z)
            print_head_x, print_head_y = head
            head = self.encode(1, rectangles, exp,
                               print_head_x, print_head_y, z)
            print_head_x, print_head_y = head

        return exp.get_instructions()

    def encode(self, num, rectangles, exp, print_head_x, print_head_y, z):
        passthroughs = []
        for rect in rectangles:
            if rect[0] == num:
                portals = []
                x_width = rect[3]-rect[1]+1
                y_width = rect[4]-rect[2]+1
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
                        'x2': rect[1] if minor_width % 2 == 0 else rect[3],
                        'y2': rect[4]
                    })
                    portals.append({
                        'x1': rect[3],
                        'y1': rect[2],
                        'x2': rect[3] if minor_width % 2 == 0 else rect[1],
                        'y2': rect[4]
                    })
                else:
                    portals.append({
                        'x1': rect[1],
                        'y1': rect[2],
                        'x2': rect[3],
                        'y2': rect[2] if minor_width % 2 == 0 else rect[4]
                    })
                    portals.append({
                        'x1': rect[1],
                        'y1': rect[4],
                        'x2': rect[3],
                        'y2': rect[4] if minor_width % 2 == 0 else rect[2]
                    })

                passthroughs.append({
                    'block': num,
                    'x1': rect[1],
                    'y1': rect[2],
                    'x2': rect[3],
                    'y2': rect[4],
                    'major': major,
                    'portals': portals
                })

        if len(passthroughs) == 0:
            return print_head_x, print_head_y

        best_time = self.calculate_deadtime(
            passthroughs, print_head_x, print_head_y)[0]
        best_pass = passthroughs.copy()
        for i in range(10000):
            random.shuffle(passthroughs)
            dead = self.calculate_deadtime(
                passthroughs, print_head_x, print_head_y)
            time = dead[0]
            if time < best_time:
                print(time)
                best_time = time
                best_pass = passthroughs.copy()

        for i in range(10000):
            a = random.randint(0, len(passthroughs)-1)
            b = random.randint(0, len(passthroughs)-1)
            passthroughs[a], passthroughs[b] = passthroughs[b], passthroughs[a]
            dead = self.calculate_deadtime(
                passthroughs, print_head_x, print_head_y)
            time = dead[0]
            if time < best_time:
                print(time)
                best_time = time
                best_pass = passthroughs.copy()

        rects = self.calculate_deadtime(
            best_pass, print_head_x, print_head_y)[2]
        head_pos = (print_head_x, print_head_y)
        block_id = {1: self.block, 2: self.support}
        for rect in rects:
            head_pos = rect['end']
            # if abs(rect['start'][0]-rect['end'][0]) == 0 and abs(rect['start'][1]-rect['end'][1]) == 0:
            #     exp.add_instruction([
            #         block_id[num],
            #         rect['start'][0], rect['start'][1], z,
            #         ])
            # elif abs(rect['start'][0]-rect['end'][0] == 0 and abs(rect['start'][1]-rect['end'][1]) == 1):
            #     exp.add_instruction([
            #         block_id[num],
            #         rect['start'][0], rect['start'][1], z,
            #         ])
            #     exp.add_instruction([
            #         block_id[num],
            #         rect['end'][0], rect['end'][1], z,
            #         ])
            # elif abs(rect['start'][0]-rect['end'][0] == 1 and abs(rect['start'][1]-rect['end'][1]) == 0):
            #     exp.add_instruction([
            #         block_id[num],
            #         rect['start'][0], rect['start'][1], z,
            #         ])
            #     exp.add_instruction([
            #         block_id[num],
            #         rect['end'][0], rect['end'][1], z,
            #         ])
            # elif abs(rect['start'][0]-rect['end'][0]) == 1 and abs(rect['start'][1]-rect['end'][1]) == 1:
            #     if rect['major'] == 'x':
            #         exp.add_instruction([
            #             block_id[num],
            #             rect['start'][0], rect['start'][1], z,
            #             ])
            #         exp.add_instruction([
            #             block_id[num],
            #             rect['end'][0], rect['start'][1], z,
            #             ])
            #         exp.add_instruction([
            #             block_id[num],
            #             rect['end'][0], rect['end'][1], z,
            #             ])
            #         exp.add_instruction([
            #             block_id[num],
            #             rect['start'][0], rect['end'][1], z,
            #             ])
            #     else:
            #         exp.add_instruction([
            #             block_id[num],
            #             rect['start'][0], rect['start'][1], z,
            #             ])
            #         exp.add_instruction([
            #             block_id[num],
            #             rect['start'][0], rect['end'][1], z,
            #             ])
            #         exp.add_instruction([
            #             block_id[num],
            #             rect['end'][0], rect['end'][1], z,
            #             ])
            #         exp.add_instruction([
            #             block_id[num],
            #             rect['end'][0], rect['start'][1], z,
            #             ])
            # else:
            if self.option2 == 'rect':
                exp.add_instruction([
                    block_id[num],
                    rect['start'][0], rect['start'][1], z,
                    rect['end'][0], rect['end'][1], z,
                    0 if rect['major'] == 'x' else 1
                ])
            elif self.option2 == 'line':
                if rect['major'] == 'x':
                    x1 = rect['start'][0]
                    x2 = rect['end'][0]
                    for y in range(rect['start'][1], rect['end'][1]+1):
                        exp.add_instruction([
                            block_id[num],
                            x1, y, z,
                            x2, y, z
                        ])
                        x1, x2 = x2, x1
                else:
                    y1 = rect['start'][1]
                    y2 = rect['end'][1]
                    for x in range(rect['start'][0], rect['end'][0]+1):
                        exp.add_instruction([
                            block_id[num],
                            x, y1, z,
                            x, y2, z
                        ])
                        y1, y2 = y2, y1
            elif self.option2 == 'none':
                if rect['major'] == 'x':
                    x1 = rect['start'][0]
                    x2 = rect['end'][0]
                    for y in range(rect['start'][1], rect['end'][1]+1):
                        for x in (range(x1, x2+1) if x1 < x2 else range(x2, x1-1, -1)):
                            exp.add_instruction([
                                block_id[num],
                                x, y, z
                            ])
                        x1, x2 = x2, x1
        return head_pos

    def calculate_deadtime(self, passthroughs, current_head_x, current_head_y):
        deadtime = []
        pos_x = current_head_x
        pos_y = current_head_y
        positions = []
        rects = []
        for passthrough in passthroughs:
            shortest_travel = None
            for portal in passthrough['portals']:
                travel = max(abs(portal['x1']-pos_x), abs(portal['y1']-pos_y))
                if shortest_travel is None or travel < shortest_travel[0]:
                    shortest_travel = (
                        travel, (portal['x2'], portal['y2']), (portal['x1'], portal['y1']))

                travel = max(abs(portal['x2']-pos_x), abs(portal['y2']-pos_y))
                if shortest_travel is None or travel < shortest_travel[0]:
                    shortest_travel = (
                        travel, (portal['x1'], portal['y1']), (portal['x2'], portal['y2']))

            deadtime.append(shortest_travel[0])
            pos_x = shortest_travel[1][0]
            pos_y = shortest_travel[1][1]
            positions.append(shortest_travel[2])
            positions.append((pos_x, pos_y))
            rects.append({'start': shortest_travel[2], 'end': (
                pos_x, pos_y), 'major': passthrough['major']})
        return sum(deadtime), positions, rects
