from util import console, parse_file_as_list, time_function
from itertools import combinations
import numpy as np

test_file = parse_file_as_list('input/11_test.txt')
day_file = parse_file_as_list('input/11.txt')


@time_function()
def run_a(file: list[str]):
    galaxies_list = np.array([[1 if char == '#' else 0 for char in line] for line in file])
    expanded_galaxies_list = expand_the_universe(galaxies_list)

    # determine galaxy coordinates
    galaxy_locations = np.where(expanded_galaxies_list == 1)

    # aligned as y, x coords
    galaxy_coords = [value for value in zip(galaxy_locations[0], galaxy_locations[1])]

    galaxy_pairs = sum([calc_manhattan_dist(pair[0], pair[1]) for pair in combinations(galaxy_coords, 2)])
    return galaxy_pairs



@time_function()
def run_b(file: list[str]):
    galaxies_list = np.array([[1 if char == '#' else 0 for char in line] for line in file])
    # determine galaxy coordinates
    galaxy_locations = np.where(galaxies_list == 1)
    galaxy_coords = [value for value in zip(galaxy_locations[0], galaxy_locations[1])]

    galaxy_coords = expand_the_universe_by_offset(galaxies_list, galaxy_coords, 1000000)

    galaxy_pairs = sum([calc_manhattan_dist(pair[0], pair[1]) for pair in combinations(galaxy_coords, 2)])
    return galaxy_pairs



# insert coordinates with y, x arrangement
def calc_manhattan_dist(coord_1: tuple, coord_2: tuple):
    x_dist = abs(coord_1[1] - coord_2[1])
    y_dist = abs(coord_1[0] - coord_2[0])
    manhattan_distance = x_dist + y_dist
    return manhattan_distance


def expand_the_universe_by_offset(galaxies_list: np.array, galaxy_coords: list[tuple], multiplier: int = 1):
    # expand vertically
    expansion_offset = 0
    multiplier = multiplier - 1 if multiplier > 1 else 1
    for index, line in enumerate(galaxies_list):
        if not any(line):
            galaxy_coords = [(coord[0] + multiplier, coord[1]) if coord[0] > (expansion_offset + index) else coord for coord in galaxy_coords ]
            expansion_offset += multiplier

    # expand vertically
    expansion_offset = 0
    for index, line in enumerate(galaxies_list.T):
        if not any(line):
            galaxy_coords = [(coord[0], coord[1] + multiplier) if coord[1] > (expansion_offset + index) else coord for coord in galaxy_coords ]
            expansion_offset += multiplier

    return galaxy_coords

def expand_the_universe(galaxies_list: np.array):
    # expand vertically
    horizontal_length = galaxies_list.shape[1]
    expanded_galaxies_list = galaxies_list.copy()
    expansion_offset = 0
    for index, line in enumerate(galaxies_list):
        if not any(line):
            index_to_insert = index + expansion_offset
            expanded_galaxies_list = np.insert(expanded_galaxies_list, index_to_insert, np.zeros((1, horizontal_length)), axis=0)
            expansion_offset += 1
    galaxies_list = expanded_galaxies_list

    # expand vertically
    vertical_length = galaxies_list.shape[0]
    expanded_galaxies_list = galaxies_list.copy()
    expansion_offset = 0
    for index, line in enumerate(galaxies_list.T):
        if not any(line):
            index_to_insert = index + expansion_offset
            expanded_galaxies_list = np.insert(expanded_galaxies_list, index_to_insert, np.zeros((1, vertical_length)), axis=1)
            expansion_offset += 1

    return expanded_galaxies_list



if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
