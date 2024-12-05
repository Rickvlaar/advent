from matplotlib.patches import Polygon
from util import console, parse_file_as_list, time_function
from graph_util import Graph
import matplotlib.pyplot as plt
import sys
import numpy as np

test_file = parse_file_as_list('input/10_test.txt')
day_file = parse_file_as_list('input/10.txt')


@time_function()
def run_a(file: list[str]):
    # read the map
    pipe_map = np.array([[char for char in line] for line in file])
    pipe_neighbours = get_possible_neighbours(pipe_map)

    the_start = np.where(pipe_map == 'S')  # Y, X
    start_coord = (the_start[0][0], the_start[1][0])

    coords_list = [(y, x) for y in range(pipe_map.shape[0]) for x in range(pipe_map.shape[1])]

    pipe_graph = Graph(start_vertex_coordinate=start_coord, vertex_neighbours_dict=pipe_neighbours)
    pipe_graph.prepare_queue_from_list(coords_list)
    pipe_graph.dijk_it()
    pipe_graph.map_dimensions = pipe_map.shape

    return max([vertex.distance for vertex in pipe_graph.coord_vertix_dict.values() if isinstance(vertex.distance, int)])


@time_function()
def run_b(file: list[str], draw_polygon=False):
    sys.setrecursionlimit(15000)

    # read the map
    pipe_map = np.array([[char for char in line] for line in file])
    pipe_neighbours = get_possible_neighbours(pipe_map)

    the_start = np.where(pipe_map == 'S')  # Y, X
    start_coord = (the_start[0][0], the_start[1][0])

    coords_list = [(y, x) for y in range(pipe_map.shape[0]) for x in range(pipe_map.shape[1])]

    pipe_graph = Graph(start_vertex_coordinate=start_coord, vertex_neighbours_dict=pipe_neighbours)
    pipe_graph.prepare_queue_from_list(coords_list)
    pipe_graph.dijk_it()
    pipe_graph.map_dimensions = pipe_map.shape

    # find all corners on the path
    paths_map = pipe_graph.plot_all_paths_on_map()

    loop_end_value = max([vertex.distance for vertex in pipe_graph.coord_vertix_dict.values() if isinstance(vertex.distance, int)])
    target_coords_wheres = np.where(paths_map == (loop_end_value - 1))
    target_coord_1 = (target_coords_wheres[0][0], target_coords_wheres[1][0])
    target_coord_2 = (target_coords_wheres[0][1], target_coords_wheres[1][1])

    path_coords = []
    target_vertex = pipe_graph.coord_vertix_dict[target_coord_1]
    pipe_graph.get_path_coordinates_to_target_vertex(path_coords, target_vertex)
    path_coords.reverse()  # needed to keep order of vertices correct

    loop_end = np.where(paths_map == loop_end_value)  # Y, X
    loop_end_coord = (loop_end[0][0], loop_end[1][0])
    path_coords.append(loop_end_coord)

    second_path_coords = []
    target_vertex = pipe_graph.coord_vertix_dict[target_coord_2]
    pipe_graph.get_path_coordinates_to_target_vertex(second_path_coords, target_vertex)
    path_coords.extend(second_path_coords)

    coordinate_symbols = {'F', '7', 'J', 'L', 'S'}
    coords_to_plot = []
    for coord in path_coords:
        vertex = pipe_graph.coord_vertix_dict[coord]
        # only plot the path
        if not isinstance(vertex.distance, int):
            continue

        if pipe_map[coord] in coordinate_symbols or coord == loop_end_coord:
            coords_to_plot.append(vertex)

    polygon_coords = []
    for vertex in coords_to_plot:
        polygon_coords.append((vertex.coordinate[1], vertex.coordinate[0]))

    if draw_polygon:
        draw_polygon_from_coords(polygon_coords, pipe_map.shape)

    area = get_polygon_surface_area_by_coords(polygon_coords)
    return int(area - loop_end_value + 1)


def get_polygon_surface_area_by_coords(polygon_coords: list[tuple]):
    # Shoelace formula https://en.wikipedia.org/wiki/Shoelace_formula
    segments = zip(polygon_coords, polygon_coords[1:] + [polygon_coords[0]])
    area = 0.5 * abs(sum(x0 * y1 - x1 * y0 for ((x0, y0), (x1, y1)) in segments))
    return area


def draw_polygon_from_coords(polygon_coords: list[tuple], shape: tuple):
    # draw the thing for fun
    polygon = Polygon(polygon_coords, color='#56B6C2', fill=False)
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))

    ax.add_patch(polygon)
    ax.set_facecolor('#353940')

    plt.ylim(shape[0] + 10, 0 - 10)
    plt.xlim(0 - 10, shape[1] + 10)

    plt.show()


def get_possible_neighbours(pipe_map: np.ndarray) -> dict:
    possible_bottoms = {'|', 'J', 'L', 'S'}
    possible_tops = {'|', 'F', '7', 'S'}
    possible_rights = {'-', '7', 'J', 'S'}
    possible_lefts = {'-', 'L', 'F', 'S'}

    max_y = pipe_map.shape[0] - 1
    max_x = pipe_map.shape[1] - 1
    the_hood = dict()
    for y, line in enumerate(pipe_map):
        for x, num in enumerate(line):
            neighbs = []
            current_pipe = pipe_map[y, x]
            # left
            if x > 0:
                left_coord = (y, x - 1)
                left = pipe_map[left_coord]
                if left in possible_lefts and current_pipe in possible_rights:
                    neighbs.append(left_coord)
            # right
            if x < max_x:
                right_coord = (y, x + 1)
                right = pipe_map[right_coord]
                if right in possible_rights and current_pipe in possible_lefts:
                    neighbs.append(right_coord)
            # top
            if y > 0:
                top_coord = (y - 1, x)
                top = pipe_map[top_coord]
                if top in possible_tops and current_pipe in possible_bottoms:
                    neighbs.append(top_coord)
            # bottom
            if y < max_y:
                bottom_coord = (y + 1, x)
                bottom = pipe_map[bottom_coord]
                if bottom in possible_bottoms and current_pipe in possible_tops:
                    neighbs.append(bottom_coord)
            the_hood[(y, x)] = neighbs

    return the_hood


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file, True)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
