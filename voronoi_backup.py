from collections import deque
from collections import defaultdict
import random
import time


def print_cube(color, point, count, f):
    point = (float(point[0]), float(point[1]), float(point[2]))
    point1 = (point[0] - 0.5, point[1] - 0.5, point[2] + 0.5)
    point2 = (point[0] - 0.5, point[1] - 0.5, point[2] - 0.5)
    point3 = (point[0] + 0.5, point[1] - 0.5, point[2] - 0.5)
    point4 = (point[0] + 0.5, point[1] - 0.5, point[2] + 0.5)
    point5 = (point[0] - 0.5, point[1] + 0.5, point[2] + 0.5)
    point6 = (point[0] + 0.5, point[1] + 0.5, point[2] + 0.5)
    point7 = (point[0] + 0.5, point[1] + 0.5, point[2] - 0.5)
    point8 = (point[0] - 0.5, point[1] + 0.5, point[2] - 0.5)

    f.write('v ' + str(point1[0]) + ' ' + str(point1[1]) + ' ' + str(point1[2]) + '\n')
    f.write('v ' + str(point2[0]) + ' ' + str(point2[1]) + ' ' + str(point2[2]) + '\n')
    f.write('v ' + str(point3[0]) + ' ' + str(point3[1]) + ' ' + str(point3[2]) + '\n')
    f.write('v ' + str(point4[0]) + ' ' + str(point4[1]) + ' ' + str(point4[2]) + '\n')
    f.write('v ' + str(point5[0]) + ' ' + str(point5[1]) + ' ' + str(point5[2]) + '\n')
    f.write('v ' + str(point6[0]) + ' ' + str(point6[1]) + ' ' + str(point6[2]) + '\n')
    f.write('v ' + str(point7[0]) + ' ' + str(point7[1]) + ' ' + str(point7[2]) + '\n')
    f.write('v ' + str(point8[0]) + ' ' + str(point8[1]) + ' ' + str(point8[2]) + '\n')

    f.write('usemtl color' + str(color) + '\n')

    f.write('f ' + str(count + 0) + ' ' + str(count + 1) + ' ' + str(count + 2) + ' ' + str(count + 3) + '\n')
    f.write('f ' + str(count + 0) + ' ' + str(count + 3) + ' ' + str(count + 5) + ' ' + str(count + 4) + '\n')
    f.write('f ' + str(count + 2) + ' ' + str(count + 6) + ' ' + str(count + 5) + ' ' + str(count + 3) + '\n')
    f.write('f ' + str(count + 4) + ' ' + str(count + 5) + ' ' + str(count + 6) + ' ' + str(count + 7) + '\n')
    f.write('f ' + str(count + 0) + ' ' + str(count + 4) + ' ' + str(count + 7) + ' ' + str(count + 1) + '\n')
    f.write('f ' + str(count + 7) + ' ' + str(count + 6) + ' ' + str(count + 2) + ' ' + str(count + 1) + '\n')


    # print point


def get_seed_point(region_number):
    global points
    global seed_points
    for seed_point in seed_points:
        if points[seed_point][1] == region_number:
            return seed_point


start = time.time()
points = {}

'''Create the dict data structure to store voxel info'''
# count = 0
is_point_line = 0
number_of_voxels = 0
last_point = None
file_name = 'bunny'
with open(file_name, 'r') as f:
    for line in f:
        if is_point_line == 0:
            number_of_voxels = int(line.strip())
            is_point_line = 1
            continue
        point_list = line.strip().split()
        point = (int(point_list[0]), int(point_list[1]), int(point_list[2]))
        last_point = point
        # print point
        '''First value is for neighbours, second value is the color of the point'''
        points[point] = (0, 0)

# print points
'''Mark existing neighbours for all the points'''
for point in points:
    starting_point = (point[0] - 1, point[1] - 1, point[2] - 1)
    # print point, starting_point
    neighbour_no = 0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                point_to_check = (starting_point[0] + i, starting_point[1] + j, starting_point[2] + k)
                if (point_to_check in points) and (point_to_check != point):
                    # print str(point_to_check) + ' is a neighbour found for ' + str(point),
                    points[point] = (points[point][0] | (1 << neighbour_no), 0)
                neighbour_no += 1

# seed_points = [(-163, 351, 162), (-37, -94, 8), (-11, 115, -102), (101, 19, -47), (173, -176, 51)]
seed_points = list()
seeds_percent = float(raw_input('Enter percentage of seed points\n'))
print seeds_percent
for point in points:
    # random_number = randint(1, number_of_voxels)
    random_number = random.uniform(0.0, 100.0)
    # if random_number < 8:
    if random_number < seeds_percent:
        seed_points.append(point)
if len(seed_points) == 0:
    seed_points.append(last_point)
print seed_points
print len(seed_points)
# seed_points = [points[1],points[5000],points[10000],points[15000],points[20000]]
adjacent_regions = defaultdict(set)
queue = deque()
region_number = 1
for point in seed_points:
    points[point] = (points[point][0], region_number)
    queue.append(point)
    # adjacent_regions[point] = list()
    region_number += 1
# print points

print adjacent_regions

# print queue
'''Incremental BFS starting from all seed points'''
while queue:
    point = queue.popleft()
    # print point
    region_number = points[point][1]
    starting_point = (point[0] - 1, point[1] - 1, point[2] - 1)
    neighbour_no = -1
    for i in range(3):
        for j in range(3):
            for k in range(3):
                neighbour_no += 1
                # print points[point], points[point][0], (1 << neighbour_no)
                if (1 << neighbour_no) & (points[point][0]):
                    # print 'Found neighbour of point ' + str(point)
                    neighbour = (starting_point[0] + i, starting_point[1] + j, starting_point[2] + k)
                    if points[neighbour][1] != 0:
                        # neighbour is already classified into a region
                        # print 'Yes'
                        if points[neighbour][1] != region_number:
                            # consider only regions other than myself
                            my_region = get_seed_point(region_number)
                            adjacent_region = get_seed_point(points[neighbour][1])
                            if adjacent_region in adjacent_regions[my_region]:
                                continue
                            # print "My region seed point: " + str(my_region)
                            # print "Just after my seed: " + str(adjacent_regions)
                            # print "Trying to add adjacent region seed point: " + str(adjacent_region)
                            # print adjacent_regions[my_region]
                            # temp_set = list()
                            # if len(adjacent_regions[my_region]) == 0:
                            #     temp_set = [adjacent_region]
                            # else:
                            #     temp_set = adjacent_regions[my_region]
                            #     temp_set = temp_set.append(adjacent_region)
                            # print abcd
                            adjacent_regions[my_region].add(adjacent_region)
                            # print "After appending: " + str(adjacent_regions)
                        continue
                    else:
                        # color neighbour and add him in the queue
                        points[neighbour] = (points[neighbour][0], region_number)
                        queue.append(neighbour)
                else:
                    continue
                # point_to_check = (starting_point[0] + i, starting_point[1] + j, starting_point[2] + k)
                # if (point_to_check in points) and (point_to_check != point):
                    # print str(point_to_check) + ' is a neighbour found for ' + str(point),
                    # points[point] = (points[point][0] | (1 << neighbour_no), 0)
                    # print '{0:026b}'.format(points[point][0])

print adjacent_regions
# for point in adjacent_regions:
#     print "List length: " + str(len(adjacent_regions[point]))
#     if len(adjacent_regions[point]) > 26:
#         print "Red alert. This is not possible"

# Now generating region-wise list of points
region_classified_points = defaultdict(list)
for seed_point in seed_points:
    region_classified_points[seed_point] = list()
for point in points:
    my_region = get_seed_point(points[point][1])
    region_classified_points[my_region].append(point)
print region_classified_points.keys()


# Now generating colors for every region
region_colors = {}
for seed_point in seed_points:
    neighbours = adjacent_regions[seed_point]
    for color in range(1, 28):
        flag = True
        for neighbour in neighbours:
            if neighbour in region_colors:
                if region_colors[neighbour] == color:
                    flag = False
                    break
            else:
                continue
        if flag:
            region_colors[seed_point] = color
            break
print region_colors


def generate_obj_file(f):
    global region_classified_points
    global seed_points
    global points
    count = 1
    for seed_point in seed_points:
        list_of_points = region_classified_points[seed_point]
        region_color = region_colors[seed_point]
        for point in list_of_points:
            if point in seed_points:
                print_cube(0, point, count, f)
                # print_cube(14, point, count, f)
            else:
                # print_cube(points[point][1] % 27 + 1, point, count, f)
                print_cube(region_color, point, count, f)
                # print_cube(14, point, count, f)
            count += 8
    # for point in points:
    #     if point in seed_points:
    #         print_cube(0, point, count, f)
    #     else:
    #         print_cube(points[point][1] % 27 + 1, point, count, f)
    #     count += 8


def generate_single_region_obj_file(f):
    global region_classified_points
    global seed_points
    global points
    count = 1
    random_seed_point = random.choice(seed_points)
    list_of_points = region_classified_points[random_seed_point]
    region_color = region_colors[random_seed_point]
    for point in list_of_points:
        if point in seed_points:
            print_cube(0, point, count, f)
        else:
            # print_cube(points[point][1] % 27 + 1, point, count, f)
            print_cube(region_color, point, count, f)
        count += 8


f = open(file_name + '.obj', 'w')
f.write('mtllib ./colorfile.mtl' + '\n')
generate_obj_file(f)
f.close()

f = open(file_name + '_single_region.obj', 'w')
f.write('mtllib ./colorfile.mtl' + '\n')
generate_single_region_obj_file(f)
f.close()

end = time.time()
print str(end - start)
