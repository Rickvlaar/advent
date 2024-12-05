import numpy as np

from util import console, parse_file_as_list, time_function

test_file = parse_file_as_list('input/16_test.txt')
day_file = parse_file_as_list('input/16.txt')


@time_function()
def run_a(file: list[str]):
    cave_map = np.array([[char for char in line] for line in file])

    # start with the first beam on top left coordinate
    start_light_beam = [(0, 0)]
    direction = ('hor', '->')
    light_beam = follow_light_beam(cave_map, start_light_beam, direction, set())

    illuminated_cave_map = np.zeros(shape=cave_map.shape)
    for coord in set(light_beam):
        illuminated_cave_map[coord] = 1

    return int(illuminated_cave_map.sum())


@time_function()
def run_b(file: list[str]):
    cave_map = np.array([[char for char in line] for line in file])

    top_starts = [((0, x_val), ('vert', 'v')) for x_val in range(cave_map.shape[1])]
    bottom_starts = [((cave_map.shape[0] - 1, x_val), ('vert', '^')) for x_val in range(cave_map.shape[1])]
    left_starts = [((y_val, 0), ('hor', '->')) for y_val in range(cave_map.shape[0])]
    right_starts = [((y_val, cave_map.shape[1] - 1), ('hor', '<-')) for y_val in range(cave_map.shape[0])]

    all_starts = top_starts + bottom_starts + left_starts + right_starts

    all_illuminated_cave_values = []
    for start_coordinate, direction in all_starts:
        # start with the first beam on top left coordinate
        start_light_beam = [start_coordinate]
        light_beam = follow_light_beam(cave_map, start_light_beam, direction, set())

        illuminated_cave_map = np.zeros(shape=cave_map.shape)
        for coord in set(light_beam):
            illuminated_cave_map[coord] = 1
        all_illuminated_cave_values.append(int(illuminated_cave_map.sum()))

    return max(all_illuminated_cave_values)


def follow_light_beam(cave_map: np.array, light_beam: list[tuple], direction: tuple, visited_splitters: set):
    current_coord = light_beam[0]
    while True:

        new_coord_value = cave_map[current_coord]
        light_beam.append(current_coord)

        # vertical split
        if new_coord_value == '|' and direction[0] == 'hor':
            direction = ('vert', 'v')
            new_beam_direction = ('vert', '^')
            new_light_beam = [current_coord]
            hit_splitter = (direction, current_coord)
            if hit_splitter in visited_splitters:
                return light_beam
            visited_splitters.add(hit_splitter)
            light_beam.extend(follow_light_beam(cave_map, new_light_beam, new_beam_direction, visited_splitters))
        # horizontal split
        elif new_coord_value == '-' and direction[0] == 'vert':
            direction = ('hor', '->')
            new_beam_direction = ('hor', '<-')
            new_light_beam = [current_coord]
            hit_splitter = (direction, current_coord)
            if hit_splitter in visited_splitters:
                return light_beam
            visited_splitters.add(hit_splitter)
            light_beam.extend(follow_light_beam(cave_map, new_light_beam, new_beam_direction, visited_splitters))
        # mirror hit
        elif new_coord_value in {'\\', '/'}:
            direction = get_new_direction_from_mirror(direction, new_coord_value)

        new_coord = get_next_coord(direction, current_coord)
        # end of the line
        if new_coord[0] in {-1, cave_map.shape[0]} or new_coord[1] in {-1, cave_map.shape[1]}:
            return light_beam

        current_coord = new_coord


def get_new_direction_from_mirror(direction: tuple, mirror: str):
    axis, heading = direction

    if axis == 'hor':
        if mirror == '\\':
            if heading == '->':
                return 'vert', 'v'
            if heading == '<-':
                return 'vert', '^'
        elif mirror == '/':
            if heading == '->':
                return 'vert', '^'
            if heading == '<-':
                return 'vert', 'v'

    if axis == 'vert':
        if mirror == '\\':
            if heading == '^':
                return 'hor', '<-'
            if heading == 'v':
                return 'hor', '->'
        elif mirror == '/':
            if heading == '^':
                return 'hor', '->'
            if heading == 'v':
                return 'hor', '<-'


def get_next_coord(direction: tuple, current_coord: tuple) -> tuple:
    axis, heading = direction

    if axis == 'hor':
        if heading == '->':
            return current_coord[0], current_coord[1] + 1
        if heading == '<-':
            return current_coord[0], current_coord[1] - 1

    if axis == 'vert':
        if heading == 'v':
            return current_coord[0] + 1, current_coord[1]
        if heading == '^':
            return current_coord[0] - 1, current_coord[1]


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
