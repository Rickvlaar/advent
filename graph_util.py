from dataclasses import field, dataclass
import numpy as np
import heapq
import math


@dataclass(order=True)
class Node:
    coordinate: tuple = field(compare=False)
    edges: list[tuple] = field(compare=False, default_factory=list)
    distance: int = field(default=math.inf)
    parent_node: 'Node' = field(compare=False, default=None)


@dataclass
class Graph:
    start_vertex_coordinate: tuple
    vertices_queue: list[Node] = field(default_factory=list)
    coord_vertix_dict: dict[tuple, Node] = field(default_factory=dict)
    vertex_neighbours_dict: dict[tuple, list[tuple]] = field(default_factory=dict)
    target_vertex_coordinate: tuple = None
    target_vertex_with_path: Node = None
    map_dimensions: tuple = None

    def prepare_queue_from_list(self, vertex_coords: list):
        neighbour_coords = self.vertex_neighbours_dict.get(self.start_vertex_coordinate)

        start_vertex = Node(coordinate=self.start_vertex_coordinate,
                            edges=neighbour_coords,
                            distance=0)
        self.coord_vertix_dict[start_vertex.coordinate] = start_vertex
        heapq.heappush(self.vertices_queue, start_vertex)

        for vertex_coord in vertex_coords:
            if vertex_coord == self.start_vertex_coordinate:
                continue

            vertex = Node(coordinate=vertex_coord,
                          edges=self.vertex_neighbours_dict.get(vertex_coord))

            self.coord_vertix_dict[vertex_coord] = vertex

    def dijk_it(self, with_target: bool = False):
        while self.vertices_queue:
            closest_vertex = heapq.heappop(self.vertices_queue)  # will be start_vertex_initially

            # do not process coordinates without neighbours
            neigbour_coords = self.vertex_neighbours_dict.get(closest_vertex.coordinate)
            if not neigbour_coords:
                continue

            # go over each neighbour and check whether the route from source vertex would be shorter
            dist_from_closest_vertex = closest_vertex.distance + 1
            for vertex_coord in neigbour_coords:
                vertex = self.coord_vertix_dict.get(vertex_coord)

                # stop processing when target is reached
                if with_target and self.is_target(vertex):
                    vertex.parent_node = closest_vertex
                    vertex.distance = dist_from_closest_vertex
                    self.target_vertex_with_path = vertex
                    return vertex.distance

                elif dist_from_closest_vertex < vertex.distance:
                    vertex.distance = dist_from_closest_vertex
                    vertex.parent_node = closest_vertex
                    heapq.heappush(self.vertices_queue, vertex)

    def is_target(self, vertex: Node):
        if vertex.coordinate == self.target_vertex_coordinate:
            return True
        else:
            return False

    def plot_path_on_map(self):
        path_map = np.full(shape=self.map_dimensions, fill_value=0, dtype=int)
        self.fill_map_from_path_vertex(path_map, self.target_vertex_with_path)
        return path_map

    def fill_map_from_path_vertex(self, path_map: np.ndarray, vertex: Node):
        path_map[vertex.coordinate] = vertex.distance
        if vertex.parent_node:
            self.fill_map_from_path_vertex(path_map, vertex.parent_node)

    def get_path_coordinates_to_target_vertex(self, coordinates: list[tuple], target_vertex: Node):
        coordinates.append(target_vertex.coordinate)
        if target_vertex.parent_node:
            self.get_path_coordinates_to_target_vertex(coordinates, target_vertex.parent_node)

    def get_all_paths_length(self):
        length = 0
        for vertex in self.coord_vertix_dict.values():
            length += 1 if isinstance(vertex.distance, int) else 0
        return length

    def plot_all_paths_on_map(self):
        paths_map = np.full(shape=self.map_dimensions, fill_value=0, dtype=int)
        for coord, vertex in self.coord_vertix_dict.items():
            paths_map[coord] = vertex.distance if isinstance(vertex.distance, int) else -1
        return paths_map

    def plot_all_paths_on_map_as_image(self):
        paths_map = np.full(shape=self.map_dimensions, fill_value=0, dtype=str)
        for coord, vertex in self.coord_vertix_dict.items():
            paths_map[coord] = '1' if isinstance(vertex.distance, int) else '.'
        return paths_map
