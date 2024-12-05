from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
from graph_util import Node
from util import get_the_hood_straight
import numpy as np
import sys

test_file = parse_file_as_list('input/23_test.txt')
day_file = parse_file_as_list('input/23.txt')


@dataclass
class NodeWithPath(Node):
    path: set[tuple] = field(default_factory=set)
    weight: int = 0


@time_function()
def run_a(file: list[str]):

    np.set_printoptions(threshold=500000)
    np.set_printoptions(linewidth=1200)
    console.width = 900
    sys.setrecursionlimit(100000)
    # np.set_printoptions(formatter={'int': lambda x: '#' if x == 0 else x})

    forest_map = convert_file_to_map(file)
    target_coord = (forest_map.shape[0] - 1, forest_map.shape[1] - 2)
    # console.print(forest_map[target_coord])

    node_edges_dict = get_the_hood_straight(forest_map, {'#'})
    start_node = NodeWithPath(
            coordinate=(0, 1),
            distance=0,
            edges=node_edges_dict.get((0, 1)),
            path={(0, 1)}
    )

    travel_map = np.zeros(shape=forest_map.shape, dtype=int)
    target_nodes = []
    follow_the_path(start_node, node_edges_dict=node_edges_dict, target_nodes=target_nodes, forest_map=forest_map, target=target_coord, travel_map=travel_map)

    target_nodes.sort(key=lambda node: node.distance, reverse=True)

    return target_nodes[0].distance


@time_function()
def run_b(file: list[str]):

    np.set_printoptions(threshold=500000)
    np.set_printoptions(linewidth=1200)
    console.width = 900
    sys.setrecursionlimit(100000)
    np.set_printoptions(formatter={'all': lambda x: f'{'$':$^3}' if x == 999 else f'{x:^3}'})

    forest_map = convert_file_to_map(file)
    target_coord = (forest_map.shape[0] - 1, forest_map.shape[1] - 2)
    # console.print(forest_map[target_coord])

    node_edges_dict = get_the_hood_straight(forest_map, {'#'})
    start_node = NodeWithPath(
            coordinate=(0, 1),
            distance=0,
            edges=node_edges_dict.get((0, 1)),
            path={(0, 1)}
    )

    travel_map = np.zeros(shape=forest_map.shape, dtype=int)
    waypoints = []
    get_node_waypoints(start_node, node_edges_dict=node_edges_dict, waypoints=waypoints, forest_map=forest_map, target=target_coord, travel_map=travel_map, previous_waypoint=start_node.coordinate)

    waypoint_nodes_dict = dict()
    waypoint_nodes_dict[(0, 1)] = NodeWithPath(
            coordinate=(0, 1),
            distance=0
    )
    waypoint_nodes_dict[target_coord] = NodeWithPath(
            coordinate=(0, 1),
            distance=0
    )

    waypoint_nodes = []

    for waypoint in waypoints:
        coordinate, distance, from_coord = waypoint
        waypoint_node = NodeWithPath(
                coordinate=coordinate,
                distance=0,
                weight=distance,
        )
        waypoint_node.edges.append((from_coord, distance))
        waypoint_nodes.append(waypoint_node)
        waypoint_nodes_dict[coordinate] = waypoint_node

    for waypoint in waypoints:
        coordinate, distance, from_coord = waypoint
        waypoint_node = waypoint_nodes_dict[from_coord]
        if (coordinate, distance) not in waypoint_node.edges:
            waypoint_node.edges.append((coordinate, distance))

        waypoint_node = waypoint_nodes_dict[coordinate]
        if (from_coord, distance) not in waypoint_node.edges:
            waypoint_node.edges.append((from_coord, distance))

    target_nodes = []
    follow_the_path_b(waypoint_nodes_dict[(0, 1)], node_edges_dict=waypoint_nodes_dict, target_nodes=target_nodes, target=target_coord)
    target_nodes.sort(key=lambda node: node.distance, reverse=True)

    return target_nodes[0].distance


def follow_the_path_b(node: NodeWithPath, node_edges_dict, target_nodes: list, target: tuple):
    for edge, weight in node.edges:
        if edge in node.path:
            continue

        edge_node = node_edges_dict.get(edge)

        new_edge_node = NodeWithPath(
                coordinate=edge,
                distance=node.distance + weight,
                path={edge} | node.path,
                edges=edge_node.edges,
                weight=edge_node.weight
        )

        if edge == target:
            target_nodes.append(new_edge_node)

        follow_the_path_b(new_edge_node, node_edges_dict, target_nodes, target)


def get_node_waypoints(node: NodeWithPath, node_edges_dict, waypoints: list, forest_map: np.array, target: tuple, travel_map, previous_waypoint):
    travel_map[node.coordinate] = node.distance

    if len(node.edges) > 2:
        travel_map[node.coordinate] = 999
        waypoints.append((node.coordinate, node.distance, previous_waypoint))
        previous_waypoint = node.coordinate
        node.distance = 0

    for edge in node.edges:
        if edge in node.path:
            continue

        direction = get_direction_from_coords(to_coord=edge, from_coord=node.coordinate)
        edge_coordinate_value = forest_map[edge]
        if edge_coordinate_value != '.':
            if direction == '<' and edge_coordinate_value == '>':
                continue
            elif direction == '^' and edge_coordinate_value == 'v':
                continue

        edge_node = NodeWithPath(
                coordinate=edge,
                distance=node.distance + 1,
                edges=node_edges_dict.get(edge),
                path={edge} | node.path
        )

        if edge_node.coordinate == target:
            travel_map[edge_node.coordinate] = 999
            waypoints.append((edge_node.coordinate, edge_node.distance, previous_waypoint))
            return

        get_node_waypoints(edge_node, node_edges_dict, waypoints, forest_map, target, travel_map, previous_waypoint)



def follow_the_path(node: NodeWithPath, node_edges_dict, target_nodes: list, forest_map: np.array, target: tuple, travel_map):
    travel_map[node.coordinate] = node.distance
    for edge in node.edges:
        if edge in node.path:
            continue

        direction = get_direction_from_coords(to_coord=edge, from_coord=node.coordinate)
        edge_coordinate_value = forest_map[edge]
        if edge_coordinate_value != '.':
            if direction == '<' and edge_coordinate_value == '>':
                continue
            elif direction == '^' and edge_coordinate_value == 'v':
                continue

        edge_node = NodeWithPath(
                coordinate=edge,
                distance=node.distance + 1,
                edges=node_edges_dict.get(edge),
                path={edge} | node.path
        )

        if edge_node.coordinate == target:
            target_nodes.append(edge_node)
            return

        follow_the_path(edge_node, node_edges_dict, target_nodes, forest_map, target, travel_map)


def get_direction_from_coords(to_coord, from_coord):
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


def convert_file_to_map(file: list[str]) -> np.array:
    return np.array([[char for char in line] for line in file])


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
