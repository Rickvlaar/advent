from util import console, parse_file_as_list, time_function
from itertools import pairwise
import numpy as np

test_file = parse_file_as_list('input/13_test.txt')
day_file = parse_file_as_list('input/13.txt')


@time_function()
def run_a(file: list[str]):
    mirror_patterns = get_mirror_patterns(file)
    mirror_indexes = get_mirror_indexes(mirror_patterns)
    return sum([index['score'] for index in mirror_indexes])


@time_function()
def run_b(file: list[str]):
    mirror_patterns = get_mirror_patterns(file)
    mirror_indexes = get_mirror_indexes(mirror_patterns)

    new_mirror_indexes = []
    for index, pattern in enumerate(mirror_patterns):
        cleaned_patterns = get_possible_smudges_for_pattern(pattern)
        new_mirror_indexes.extend(get_mirror_indexes_b(cleaned_patterns, mirror_indexes[index]))

    return sum([index['score'] for index in new_mirror_indexes])


def get_possible_smudges_for_pattern(pattern: np.array):
    new_patterns = []

    for line_index, line in enumerate(pattern):
        for index, symbol in enumerate(line):
            pattern_copy = pattern.copy()
            line_1_copy = line.copy()
            line_1_copy[index] = '.' if symbol == '#' else '#'
            pattern_copy[line_index] = line_1_copy
            new_patterns.append(pattern_copy)
    return new_patterns


def get_mirror_indexes(mirror_patterns):
    mirror_indexes = []

    # row matches
    for pattern in mirror_patterns:
        index = 0
        for line_index, line_pair in enumerate(pairwise(pattern)):


            line_1, line_2 = line_pair

            if np.array_equal(line_1, line_2):
                if check_if_actual_mirror(pattern, index):
                    mirror_indexes.append({'dir':   'row',
                                           'index': line_index,
                                           'score': (line_index + 1) * 100
                                           })
                    break
            index += 1

        # column matches
        index = 0
        for line_index, line_pair in enumerate(pairwise(pattern.T)):

            line_1, line_2 = line_pair

            if np.array_equal(line_1, line_2):
                if check_if_actual_mirror(pattern.T, index):
                    mirror_indexes.append({'dir':   'col',
                                           'index': index,
                                           'score': (index + 1)
                                           })
                    break
            index += 1

    return mirror_indexes


def get_mirror_indexes_b(mirror_patterns, original_mirror_details):
    mirror_indexes = []

    # row matches
    for pattern in mirror_patterns:
        index = 0
        for line_index, line_pair in enumerate(pairwise(pattern)):
            if original_mirror_details['index'] == line_index and original_mirror_details['dir'] == 'row':
                continue

            line_1, line_2 = line_pair

            if np.array_equal(line_1, line_2):
                if check_if_actual_mirror(pattern, line_index):
                    mirror_indexes.append({'dir':   'row',
                                           'index': line_index,
                                           'score': (line_index + 1) * 100
                                           })
                    return mirror_indexes
            index += 1

        # column matches
        index = 0
        for line_index, line_pair in enumerate(pairwise(pattern.T)):
            if original_mirror_details['index'] == line_index and original_mirror_details['dir'] == 'col':
                continue

            line_1, line_2 = line_pair

            if np.array_equal(line_1, line_2):
                if check_if_actual_mirror(pattern.T, line_index):
                    mirror_indexes.append({'dir':   'col',
                                           'index': line_index,
                                           'score': (line_index + 1)
                                           })
                    return mirror_indexes
            index += 1
    return mirror_indexes


def check_if_actual_mirror(mirror_pattern: np.array, hit_index):
    mirror_left = mirror_pattern[:hit_index + 1]
    mirror_right = mirror_pattern[hit_index + 1:]
    shortest_len = min(len(mirror_left), len(mirror_right))

    flipped_left = np.flipud(mirror_left)
    for index in range(shortest_len):
        if not np.array_equal(flipped_left[index], mirror_right[index]):
            return False

    return True


def get_mirror_patterns(file: list[str]):
    patterns = []
    sub_pattern = []
    for line in file:
        if line:
            sub_pattern.append([val for val in line])
        else:
            patterns.append(np.array(sub_pattern))
            sub_pattern = []
    patterns.append(np.array(sub_pattern))

    return patterns


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
