from util import console, parse_file_as_list, time_function

test_file = parse_file_as_list('input/18_test.txt')
day_file = parse_file_as_list('input/18.txt')


@time_function()
def run_a(file: list[str]):
    dig_instructions = convert_lines_instructions_a(file)
    return determine_trench_size(dig_instructions)


@time_function()
def run_b(file: list[str]):
    dig_instructions = convert_lines_instructions_b(file)
    return determine_trench_size(dig_instructions)


def determine_trench_size(dig_instructions: list[tuple]) -> int:
    hole_coords = [(0, 0)]
    coord = hole_coords[0]
    trench_len = 0
    for direction, distance in dig_instructions:
        coord = get_destination_coord_for_direction_and_distance(coord, direction, distance)
        trench_len += distance
        hole_coords.append(coord)

    x_y_coords = [(coord[1], coord[0]) for coord in hole_coords]
    return int(get_polygon_surface_area_by_coords(x_y_coords) + (trench_len / 2) + 1)


def convert_lines_instructions_a(file: list[str]):
    return [(splitline[0], int(splitline[1])) for splitline in [line.split(' ') for line in file]]


def convert_lines_instructions_b(file: list[str]):
    code_direction_dict = {
            '0': 'R',
            '1': 'D',
            '2': 'L',
            '3': 'U'
    }

    return [(code_direction_dict[splitline[2][-2]], int(splitline[2][2:-2], 16)) for splitline in [line.split(' ') for line in file]]


def get_destination_coord_for_direction_and_distance(coord: tuple, direction: str, distance: int):
    if direction == 'R':
        return coord[0], coord[1] + distance
    elif direction == 'L':
        return coord[0], coord[1] - distance
    elif direction == 'D':
        return coord[0] + distance, coord[1]
    elif direction == 'U':
        return coord[0] - distance, coord[1]


def get_polygon_surface_area_by_coords(polygon_coords: list[tuple]):
    # Shoelace formula https://en.wikipedia.org/wiki/Shoelace_formula
    segments = zip(polygon_coords, polygon_coords[1:] + [polygon_coords[0]])
    area = 0.5 * abs(sum(x0 * y1 - x1 * y0 for ((x0, y0), (x1, y1)) in segments))
    return area


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
