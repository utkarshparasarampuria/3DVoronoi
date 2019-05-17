from collections import deque
from collections import defaultdict
import random
import time

number_of_voxels = 0
points = {}


def parse_input(filename):
    '''Create the dict data structure to store voxel info'''
    global number_of_voxels
    global points

    is_point_line = 0
    with open(filename, 'r') as f:
        for line in f:
            if is_point_line == 0:
                number_of_voxels = int(line.strip())
                is_point_line = 1
                continue
            point_list = line.strip().split()
            point = (int(point_list[0]), int(point_list[1]), int(point_list[2]))
            # last_point = point
            # print point
            '''First value is for neighbours, second value is the color of the point'''
            points[point] = (0, 0)
    return


def mark_neighbors():
    global points

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
    return


def random_seeds(percent):
    global points

    seed_points = list()
    for point in points:
        # random_number = randint(1, number_of_voxels)
        random_number = random.uniform(0.0, 100.0)
        # if random_number < 8:
        if random_number < percent:
            seed_points.append(point)
    return seed_points


def get_seed_point(region_number, seed_points):
    global points
    for seed_point in seed_points:
        if points[seed_point][1] == region_number:
            return seed_point


def incremental_bfs(seed_points):
    global points

    # Initialisation of points to no regions
    for point in points:
        points[point] = (points[point][0], 0)

    # Return variables and helper variables
    adjacent_regions = defaultdict(set)
    boundary_points = defaultdict(set)
    queue = deque()
    region_number = 1

    # Fill queue with only seed points to start
    for point in seed_points:
        points[point] = (points[point][0], region_number)
        queue.append(point)
        region_number += 1

    # Incremental BFS starting from all seed points
    while queue:
        point = queue.popleft()
        region_number = points[point][1]
        starting_point = (point[0] - 1, point[1] - 1, point[2] - 1)
        neighbour_no = -1
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    neighbour_no += 1
                    if (1 << neighbour_no) & (points[point][0]):
                        # print 'Found neighbour of point ' + str(point)
                        neighbour = (starting_point[0] + i, starting_point[1] + j, starting_point[2] + k)
                        if points[neighbour][1] != 0:
                            # neighbour is already classified into a region
                            if points[neighbour][1] != region_number:
                                # consider only regions other than myself
                                # this means I am a boundary point
                                my_region = get_seed_point(region_number, seed_points)
                                adjacent_region = get_seed_point(points[neighbour][1], seed_points)
                                boundary_points[my_region].add(point)
                                if adjacent_region in adjacent_regions[my_region]:
                                    continue
                                adjacent_regions[my_region].add(adjacent_region)
                            continue
                        else:
                            # color neighbour and add him in the queue
                            points[neighbour] = (points[neighbour][0], region_number)
                            queue.append(neighbour)
                    else:
                        continue

    return adjacent_regions, boundary_points


def classify(seed_points):
    global points

    region_classified_points = defaultdict(list)
    for seed_point in seed_points:
        region_classified_points[seed_point] = list()
    for point in points:
        my_region = get_seed_point(points[point][1], seed_points)
        region_classified_points[my_region].append(point)
    print region_classified_points.keys()
    return region_classified_points


def assign_colors(seed_points, adjacent_regions):
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
    return region_colors


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

    return


def generate_obj_file(f, seed_points, voronoi_cells, region_colors):
    count = 1
    for seed_point in seed_points:
        list_of_points = voronoi_cells[seed_point]
        region_color = region_colors[seed_point]
        for point in list_of_points:
            if point in seed_points:
                print_cube(0, point, count, f)
                # print_cube(14, point, count, f)
            else:
                # print_cube(points[point][1] % 27 + 1, point, count, f)
                print_cube(region_color, point, count, f)
            count += 8
    return


def manhattan_distance(p1, p2):
    distance = abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2])
    return distance


def get_max_distance_difference(point, boundary):
    # result = 0.0
    min_distance = float('inf')
    max_distance = float('-inf')
    for point2 in boundary:
        distance = manhattan_distance(point, point2)
        if distance > max_distance:
            max_distance = distance
        if distance < min_distance:
            min_distance = distance
    result = max_distance - min_distance
    return result


def generate_new_seeds(seed_points, voronoi_cells, boundary_points):
    new_seed_points = {}
    for seed in seed_points:
        region = voronoi_cells[seed]
        boundary = boundary_points[seed]
        new_seed = seed
        min_difference = float('inf')
        for point in region:
            difference = get_max_distance_difference(point, boundary)
            if difference < min_difference:
                new_seed = point
        new_seed_points[seed] = new_seed
    return new_seed_points


def change_seeds(new_seed_points, region_colors):
    new_region_colors = {}
    new_seeds = list()
    for seed in new_seed_points:
        new_seed = new_seed_points[seed]
        color = region_colors[seed]
        new_region_colors[new_seed] = color
        new_seeds.append(new_seed)
    return new_seeds, new_region_colors


def find_color(colors, neighbors):
    color = 1
    for i in range(27):
        flag = False
        for neighbor in neighbors:
            neighbor_color = colors[neighbor]
            if color == neighbor_color:
                flag = True
                break
        if flag:
            color += 1
        else:
            return color


def recolor(seed_points, region_colors, adjacent_regions):
    new_colors = {}
    for seed in seed_points:
        neighbors = adjacent_regions[seed]
        my_color = region_colors[seed]
        flag = False
        for neighbor in neighbors:
            if region_colors[neighbor] == my_color:
                flag = True
                break
        if flag:
            my_color = find_color(region_colors, neighbors)
            region_colors[seed] = my_color
        new_colors[seed] = my_color
    return new_colors


def main():
    input_filename = 'bunny'
    seed_points = list()
    region_colors = {}
    max_iterations = 10

    print 'Reading input file'
    parse_input(input_filename)

    print 'Marking neighbors'
    mark_neighbors()

    print 'Initial random seeding'
    seeds_percent = float(raw_input('Enter percentage of seed points\n'))
    print seeds_percent
    seed_points = random_seeds(seeds_percent)
    print seed_points
    print len(seed_points)

    print 'Starting iterations'
    for i in range(max_iterations):
        print 'Iteration number: ' + str(i+1)
        adjacent_regions, boundary_points = incremental_bfs(seed_points)
        voronoi_cells = classify(seed_points)
        if i == 0:
            region_colors = assign_colors(seed_points, adjacent_regions)
        else:
            region_colors = recolor(seed_points, region_colors, adjacent_regions)

        f = open(input_filename + str(i+1) + '.obj', 'w')
        f.write('mtllib ./colorfile.mtl' + '\n')
        generate_obj_file(f, seed_points, voronoi_cells, region_colors)
        f.close()

        # f = open(input_filename + '_boundary_points.obj', 'w')
        # f.write('mtllib ./colorfile.mtl' + '\n')
        # generate_obj_file(f, seed_points, boundary_points, region_colors)
        # f.close()

        print 'Generating new seeds'
        new_seed_points = generate_new_seeds(seed_points, voronoi_cells, boundary_points)
        if new_seed_points in seed_points and seed_points in new_seed_points:
            print 'New seeds are same as old seeds'
            print 'Stopping iterations'
            break
        seed_points, region_colors = change_seeds(new_seed_points, region_colors)
        # seed_points = change_seeds(new_seed_points)
    return


start = time.time()
main()
end = time.time()
print 'Total time taken: ' + str(end - start)
