import numpy as np

from util import console, parse_file_as_list, time_function

test_file = parse_file_as_list('input/14_test.txt')
day_file = parse_file_as_list('input/14.txt')

ROLL_ROCK = 'O'
BLOCK_ROCK = '#'


@time_function()
def run_a(file: list[str]):
    mirror_array = np.array([[char for char in line] for line in file])

    # transposed array has north on y-axis 0-index
    roll_rock_north_orientation_left(mirror_array.T)

    return calculate_load(mirror_array)


@time_function()
def run_b(file: list[str]):
    mirror_array = np.array([[char for char in line] for line in file])

    total_cycles = 1000000000  # 1 billion
    repeats_at_cycle, matched_cycle = cycle_until_repeating_output(mirror_array)
    remaining_cycles = (total_cycles - matched_cycle) % (repeats_at_cycle - matched_cycle)

    for _ in range(remaining_cycles):
        do_roll_cycle(mirror_array)

    return calculate_load(mirror_array)


def cycle_until_repeating_output(mirror_array: np.array):
    arrays_after_cycles = []
    cycle = 0
    while True:
        cycled_array = do_roll_cycle(mirror_array).copy()
        cycle += 1
        for known_arr_index, known_array in enumerate(arrays_after_cycles):
            # Check at which cycle history repeats itself
            if np.array_equal(cycled_array, known_array):
                return cycle, known_arr_index + 1
        arrays_after_cycles.append(cycled_array)


# each cycle tilts 4 time n->w->s->e
def do_roll_cycle(mirror_array: np.array):
    roll_rock_north_orientation_left(mirror_array.T)
    for _ in range(3):
        # transposed array has north on y-axis 0-index
        mirror_array = np.rot90(mirror_array, k=-1)
        roll_rock_north_orientation_left(mirror_array.T)
    # return north side up
    return np.rot90(mirror_array, k=-1)


# the array must be oriented to left side of array
def roll_rock_north_orientation_left(north_left_mirror_array: np.array):
    for y_index, mirror_line in enumerate(north_left_mirror_array):
        index_of_nearest_blocker = -1
        for symbol_index, symbol in enumerate(mirror_line):
            # move the rock as far left as possible
            if symbol == ROLL_ROCK:
                new_location_index = index_of_nearest_blocker + 1
                mirror_line[new_location_index] = ROLL_ROCK
                # if rolling rock has move clear original position
                if symbol_index != new_location_index:
                    mirror_line[symbol_index] = '.'
                # set new blocker location
                if index_of_nearest_blocker != new_location_index:
                    index_of_nearest_blocker = new_location_index

            # if hitting a block, just set the newest blocker index
            elif symbol == BLOCK_ROCK:
                index_of_nearest_blocker = symbol_index
    return north_left_mirror_array


def calculate_load(mirror_array: np.array):
    # calculate load, flip upside down so enumeration is easier
    north_bottom_mirror_array = np.flipud(mirror_array)
    total_load = 0
    for line_load_value, mirror_line in enumerate(north_bottom_mirror_array, start=1):
        total_load += np.count_nonzero(mirror_line == ROLL_ROCK) * line_load_value
    return total_load


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
