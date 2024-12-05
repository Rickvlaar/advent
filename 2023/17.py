from util import console, parse_file_as_list, time_function, get_the_hood_straight, calc_manhattan_dist
from graph_util import Graph, Node
from dataclasses import field, dataclass
from itertools import pairwise
import heapq
import numpy as np
import math

test_file = parse_file_as_list('input/17_test.txt')
day_file = parse_file_as_list('input/17.txt')
test_sol = parse_file_as_list('input/17_test_solution.txt')


@dataclass(order=True)
class Vertex:
    coordinate: tuple = field(compare=False)
    neighbours: list[tuple] = field(compare=False, default_factory=list)
    distance: int = field(default=math.inf)
    weight: int = field(compare=False, default=0)
    direction: str = field(compare=False, default=None)
    stay_on_track: bool = field(compare=False, default=True)
    divert: bool = field(compare=False, default=False)
    steps_in_direction: int = field(compare=False, default=0)
    previous_vertex: 'Node' = field(compare=False, default=None)

    def get_left_neighbour_coord(self):
        return self.coordinate[0], self.coordinate[1] - 1

    def get_top_neighbour_coord(self):
        return self.coordinate[0] - 1, self.coordinate[1]

    def get_right_neighbour_coord(self):
        return self.coordinate[0], self.coordinate[1] + 1

    def get_bottom_neighbour_coord(self):
        return self.coordinate[0] + 1, self.coordinate[1]

    def get_path_history(self, steps: int, path_history_steps: list, current_step: int = 0):
        if current_step == steps or self.previous_vertex is None:
            return path_history_steps

        path_history_steps.append(self.previous_vertex.coordinate)
        current_step += 1
        return self.previous_vertex.get_path_history(steps, path_history_steps, current_step)


@dataclass
class Graph:
    start_vertex_coordinate: tuple
    vertices_queue: list[Vertex] = field(default_factory=list)
    coord_vertix_dict: dict[tuple, Vertex] = field(default_factory=dict)
    vertex_neighbours_dict: dict[tuple, list[tuple]] = field(default_factory=dict)
    map: np.array = None
    target_vertex_coordinate: tuple = None
    target_vertex_with_path: Vertex = None
    map_dimensions: tuple = None

    def prepare_queue_from_coord_value_dict(self, coord_weight_dict: dict[tuple: int]):
        neighbour_coords = self.vertex_neighbours_dict.get(self.start_vertex_coordinate)

        start_vertex = Node(coordinate=self.start_vertex_coordinate,
                            edges=neighbour_coords,
                            distance=0,
                            weight=0)

        self.coord_vertix_dict[start_vertex.coordinate] = start_vertex

        heapq.heappush(self.vertices_queue, start_vertex)

        # for vertex_coord, weight in coord_weight_dict.items():
        #     if vertex_coord == self.start_vertex_coordinate:
        #         continue
        #
        #     for direction in '<>v^':
        #         for step in range(1, 11):
        #             vertex = Vertex(coordinate=vertex_coord,
        #                             direction=direction,
        #                             divert=step == 10,
        #                             neighbours=self.vertex_neighbours_dict.get(vertex_coord),
        #                             stay_on_track=step < 4,
        #                             steps_in_direction=step,
        #                             weight=weight)
        #
        #             vertex_direction_tuple = (vertex_coord, direction, step)
        #             self.coord_vertix_dict[vertex_direction_tuple] = vertex

    def dijk_it(self, with_target: bool = False):
        while self.vertices_queue:
            closest_vertex = heapq.heappop(self.vertices_queue)  # will be start_vertex_initially

            # do not process coordinates without neighbours
            neigbour_coords = self.vertex_neighbours_dict.get(closest_vertex.coordinate)
            if not neigbour_coords:
                continue

            # go over each neighbour and check whether the route from source vertex would be shorter
            for neighbour_vertex_coord in neigbour_coords:
                # prevents backtracking
                if closest_vertex.previous_vertex and neighbour_vertex_coord == closest_vertex.previous_vertex.coordinate or neighbour_vertex_coord == self.start_vertex_coordinate:
                    continue

                neigh_dir = self.get_direction_from_coords(neighbour_vertex_coord, closest_vertex.coordinate)
                if closest_vertex.stay_on_track and closest_vertex.coordinate != self.start_vertex_coordinate:
                    if neigh_dir != closest_vertex.direction:
                        continue

                elif closest_vertex.divert:
                    if closest_vertex.direction == '^' and closest_vertex.get_top_neighbour_coord() == neighbour_vertex_coord:
                        continue
                    elif closest_vertex.direction == '<' and closest_vertex.get_left_neighbour_coord() == neighbour_vertex_coord:
                        continue
                    elif closest_vertex.direction == '>' and closest_vertex.get_right_neighbour_coord() == neighbour_vertex_coord:
                        continue
                    elif closest_vertex.direction == 'v' and closest_vertex.get_bottom_neighbour_coord() == neighbour_vertex_coord:
                        continue

                neigh_steps = closest_vertex.steps_in_direction + 1 if neigh_dir == closest_vertex.direction else 1

                neigh_vertex_key = (neighbour_vertex_coord, neigh_dir, neigh_steps)
                if neigh_vertex_key in self.coord_vertix_dict:
                    vertex = self.coord_vertix_dict.get(neigh_vertex_key)
                else:
                    vertex = Node(coordinate=neighbour_vertex_coord,
                                  direction=neigh_dir,
                                  divert=neigh_steps == 10,
                                  edges=self.vertex_neighbours_dict.get(neighbour_vertex_coord),
                                  stay_on_track=neigh_steps < 4,
                                  steps_in_direction=neigh_steps,
                                  weight=self.map[neighbour_vertex_coord])
                    self.coord_vertix_dict[neigh_vertex_key] = vertex

                dist_from_closest_vertex = closest_vertex.distance + vertex.weight

                # stop processing when target is reached
                if with_target and self.is_target(vertex):
                    if vertex.steps_in_direction < 4:
                        continue

                    vertex.parent_node = closest_vertex
                    vertex.distance = dist_from_closest_vertex
                    self.target_vertex_with_path = vertex
                    return vertex.distance

                if dist_from_closest_vertex < vertex.distance:
                    vertex.distance = dist_from_closest_vertex
                    vertex.parent_node = closest_vertex
                    heapq.heappush(self.vertices_queue, vertex)

    def is_target(self, vertex: Vertex):
        if vertex.coordinate == self.target_vertex_coordinate:
            return True
        else:
            return False

    def get_direction_from_coords(self, to_coord, from_coord):
        y_change = to_coord[0] - from_coord[0]
        x_change = to_coord[1] - from_coord[1]
        direction = ''
        if y_change == -1:  # moving up
            direction = '^'
        elif y_change == 1:  # moving down
            direction = 'v'
        elif x_change == -1:  # moving left
            direction = '<'
        elif x_change == 1:  # moving right
            direction = '>'
        return direction

    def get_steps_in_same_direction(self, history, current_direction, steps_back: int):
        same_direction_steps = 1
        for coord, coord_before in pairwise(history):
            direction = self.get_direction_from_coords(coord, coord_before)

            if current_direction == direction:
                same_direction_steps += 1
            else:
                break

        return same_direction_steps

    def get_combined_weights(self, weight: int, vertex: Vertex):
        weight += vertex.weight
        if vertex.previous_vertex:
            weight = self.get_combined_weights(weight, vertex.previous_vertex)
        return weight

    def get_path_coordinates_to_target_vertex(self, coordinates: list[tuple], target_vertex: Vertex):
        coordinates.append(target_vertex.coordinate)
        if target_vertex.previous_vertex:
            self.get_path_coordinates_to_target_vertex(coordinates, target_vertex.previous_vertex)

    def get_all_paths_length(self):
        length = 0
        for vertex in self.coord_vertix_dict.values():
            length += 1 if isinstance(vertex.distance, int) else 0
        return length

    def plot_path_on_map(self):
        path_map = np.full(shape=self.map_dimensions, fill_value=0, dtype=int)
        self.fill_map_from_path_vertex(path_map, self.target_vertex_with_path)
        return path_map

    def fill_map_from_path_vertex(self, path_map: np.ndarray, vertex: Vertex):
        path_map[vertex.coordinate] = vertex.distance
        if vertex.previous_vertex:
            self.fill_map_from_path_vertex(path_map, vertex.previous_vertex)

    def plot_all_paths_on_map(self):
        paths_map = np.full(shape=self.map_dimensions, fill_value=0, dtype=int)
        for vertex in self.coord_vertix_dict.values():
            paths_map[vertex.coordinate] = vertex.distance if vertex.distance != math.inf else -1
        return paths_map

    def plot_all_paths_on_map_as_image(self):
        paths_map = np.full(shape=self.map_dimensions, fill_value=0, dtype=str)
        for coord, vertex in self.coord_vertix_dict.items():
            paths_map[coord] = '1' if isinstance(vertex.distance, int) else '.'
        return paths_map


@time_function()
def run_a(file: list[str]):
    lava_map = np.array([[int(char) for char in line] for line in file])

    coords_value_dict = {(y, x): lava_map[y, x] for y in range(lava_map.shape[0]) for x in range(lava_map.shape[1])}
    lava_neighbours = get_the_hood_straight(lava_map)
    lava_graph = Graph(start_vertex_coordinate=(0, 0), vertex_neighbours_dict=lava_neighbours)
    lava_graph.target_vertex_coordinate = (lava_map.shape[0] - 1, lava_map.shape[1] - 1)
    lava_graph.prepare_queue_from_coord_value_dict(coords_value_dict)
    lava_graph.map = lava_map
    lava_graph.map_dimensions = lava_map.shape
    lava_graph.dijk_it(with_target=True)

    return lava_graph.get_combined_weights(0, lava_graph.target_vertex_with_path)


@time_function()
def run_b(file: list[str]):
    lava_map = np.array([[int(char) for char in line] for line in file])

    coords_value_dict = {(y, x): lava_map[y, x] for y in range(lava_map.shape[0]) for x in range(lava_map.shape[1])}
    lava_neighbours = get_the_hood_straight(lava_map)
    lava_graph = Graph(start_vertex_coordinate=(0, 0), vertex_neighbours_dict=lava_neighbours)
    lava_graph.target_vertex_coordinate = (lava_map.shape[0] - 1, lava_map.shape[1] - 1)
    lava_graph.prepare_queue_from_coord_value_dict(coords_value_dict)
    lava_graph.map = lava_map
    lava_graph.map_dimensions = lava_map.shape
    lava_graph.dijk_it(with_target=True)

    return lava_graph.get_combined_weights(0, lava_graph.target_vertex_with_path)


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
