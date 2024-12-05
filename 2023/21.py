import heapq
import numpy as np
import math
from util import console, parse_file_as_list, time_function, calc_manhattan_dist, get_the_hood_straight
from dataclasses import field, dataclass
from graph_util import Graph

test_file = parse_file_as_list('input/21_test.txt')
day_file = parse_file_as_list('input/21.txt')


@dataclass(order=True)
class Node:
    coordinate: tuple = field(compare=False)
    distance: int = field(default=math.inf, compare=False)
    predicted_distance_to_target: int = field(default=math.inf)
    edges: list[tuple] = field(compare=False, default_factory=list)
    parent_node: 'Node' = field(compare=False, default=None)

    def __post_init__(self):
        self.set_edges()

    def set_edges(self):
        y, x = self.coordinate
        self.edges.append((y, x - 1))
        self.edges.append((y, x + 1))
        self.edges.append((y - 1, x))
        self.edges.append((y + 1, x))


@dataclass
class AStar:
    the_map: np.array
    start_coord: tuple
    target_coord: tuple
    max_dist: int = 64
    node_queue: list[Node] = field(default_factory=list)
    known_nodes: dict[str: Node] = field(default_factory=dict)

    def __post_init__(self):
        heapq.heapify(self.node_queue)
        start_node = Node(
                coordinate=self.start_coord,
                distance=0,
                predicted_distance_to_target=calc_manhattan_dist(self.start_coord, self.target_coord)
        )
        self.known_nodes[self.start_coord] = start_node
        heapq.heappush(self.node_queue, start_node)

    def compute_shortest_path(self):
        while self.node_queue:
            current_node = heapq.heappop(self.node_queue)

            if current_node.coordinate == self.target_coord:
                return current_node

            for neighbour_coord in current_node.edges:
                map_value = self.the_map[neighbour_coord]
                # cannot pass rocks
                if not map_value:
                    continue

                predicted_distance_to_target = calc_manhattan_dist(neighbour_coord, self.target_coord)
                distance_to_neighbour = current_node.distance + 1

                # do not travel too far
                if distance_to_neighbour > self.max_dist:
                    continue

                if neighbour_coord in self.known_nodes:
                    neighbour_node = self.known_nodes[neighbour_coord]
                else:
                    neighbour_node = Node(coordinate=neighbour_coord)
                    self.known_nodes[neighbour_coord] = neighbour_node

                if distance_to_neighbour < neighbour_node.distance:
                    neighbour_node.parent_node = current_node
                    neighbour_node.distance = distance_to_neighbour
                    neighbour_node.predicted_distance_to_target = predicted_distance_to_target
                    heapq.heappush(self.node_queue, neighbour_node)

        return False


@time_function()
def run_a(file: list[str]):
    garder_map_coord = np.array([[char for char in line] for line in file])
    the_start = np.where(garder_map_coord == 'S')  # Y, X
    start_coord = (the_start[0][0], the_start[1][0])

    garden_map = get_garden_map(file)
    np.set_printoptions(threshold=math.inf)
    np.set_printoptions(linewidth=1200)
    console.width = 900

    neighbour_dict = get_the_hood_straight(garden_map, {0})
    garden_graph = Graph(
            start_vertex_coordinate=start_coord,
            vertex_neighbours_dict=neighbour_dict,
            map_dimensions=garden_map.shape
    )
    coords_list = [(y, x) for y in range(garden_map.shape[0]) for x in range(garden_map.shape[1])]
    garden_graph.prepare_queue_from_list(coords_list)
    garden_graph.dijk_it()
    all_paths_map = garden_graph.plot_all_paths_on_map()

    max_steps = 64
    possible_locations = []
    for y, line in enumerate(garden_map):
        for x, char in enumerate(line):
            distance = all_paths_map[y, x]
            if distance % 2 != 0:
                continue

            if 0 <= distance <= max_steps:
                possible_locations.append((y, x))
                garder_map_coord[y, x] = 'X'

    return len(possible_locations)


@time_function()
def run_b(file: list[str]):
    garden_map = get_garden_map(file)
    repeated = np.tile(garden_map, (7, 7))
    start_coord = (math.floor(repeated.shape[0] / 2), math.floor(repeated.shape[0] / 2))
    neighbour_dict = get_the_hood_straight(repeated, {0})

    garden_graph = Graph(
            start_vertex_coordinate=start_coord,
            vertex_neighbours_dict=neighbour_dict,
            map_dimensions=repeated.shape
    )

    coords_list = [(y, x) for y in range(repeated.shape[0]) for x in range(repeated.shape[1])]
    garden_graph.prepare_queue_from_list(coords_list)
    garden_graph.dijk_it()
    all_paths_map = garden_graph.plot_all_paths_on_map()

    vertical_split = np.vsplit(all_paths_map, 7)
    all_nine = np.array([np.hsplit(vert_s, 7) for vert_s in vertical_split])

    corners = [all_nine[2, 2],
               all_nine[2, 4],
               all_nine[4, 2],
               all_nine[4, 4]]
    straights = [all_nine[0, 3],
                 all_nine[3, 0],
                 all_nine[3, 6],
                 all_nine[6, 3]]

    max_steps = 26501365
    max_steps_in_even_map = 0
    is_even = False
    for y, line in enumerate(all_nine[3, 3]):
        for x, distance in enumerate(line):
            if is_valid_garden_position_even(distance, max_steps, is_even):
                if 0 <= distance <= max_steps:
                    max_steps_in_even_map += 1

    max_steps_in_odd_map = 0
    for y, line in enumerate(all_nine[3, 4]):
        for x, distance in enumerate(line):
            if is_valid_garden_position_even(distance, max_steps, is_even):
                if 0 <= distance <= max_steps:
                    max_steps_in_odd_map += 1

    map_edge_length = garden_map.shape[0]

    max_blocks_in_direction = (max_steps // map_edge_length)
    even_blocks = 1 if max_blocks_in_direction >= 1 else 0
    odd_blocks = 0
    for expansion in range(max_blocks_in_direction - 1):
        if expansion % 2 == 0:
            even_blocks += expansion * 4
        else:
            odd_blocks += expansion * 4

    evens = even_blocks * max_steps_in_even_map
    odds = odd_blocks * max_steps_in_odd_map

    possible_locations_new = evens + odds
    possible_locations_new += get_possible_placements(straights, corners, map_edge_length, max_steps, expansion_level=max_blocks_in_direction-4, is_even=is_even)

    return possible_locations_new


def is_valid_garden_position_even(distance: int, max_steps: int, is_even: bool = True):
    if distance % 2 != 0 and is_even:
        return False
    elif distance % 2 == 0 and not is_even:
        return False
    elif 0 <= distance <= max_steps:
        return True
    else:
        return False


def get_possible_placements(straights, corners, map_edge_length, max_steps, expansion_level, is_even=True):
    possible_locations = 0
    while True:
        still_adding = False

        for corner in corners:
            for y, corner_line in enumerate(corner):
                for x, distance in enumerate(corner_line):
                    if distance == -1:
                        continue
                    distance_modifier = map_edge_length * (expansion_level + 1)
                    distance += distance_modifier
                    if is_valid_garden_position_even(distance, max_steps, is_even):
                        still_adding = True
                        possible_locations += expansion_level + 2

        for straight in straights:
            for y, line in enumerate(straight):
                for x, distance in enumerate(line):
                    if distance == -1:
                        continue
                    distance_modifier = map_edge_length * expansion_level
                    distance += distance_modifier
                    if is_valid_garden_position_even(distance, max_steps, is_even):
                        still_adding = True
                        possible_locations += 1

        if not still_adding:
            break

        expansion_level += 1
    return possible_locations


def get_garden_map(file: list[str]):
    return np.array([[0 if char == '#' else 1 for char in line] for line in file])


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
