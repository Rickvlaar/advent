import itertools

from util import console, parse_file_as_list, time_function
from itertools import combinations, product, permutations, pairwise
from dataclasses import dataclass, field
from math import prod
import re

test_file = parse_file_as_list('input/12_test.txt')
day_file = parse_file_as_list('input/12.txt')


@time_function()
def run_a(file: list[str]):
    spring_view_strings, arrangements = split_spring_view_from_arrangements(file)


    for index, spring_view_string in enumerate(spring_view_strings):
        process_spring_view(spring_view_string, arrangements[index])


    test = '????'
    print(test[4:])
    print(get_group_size(test[3:]))
    print(get_min_group_size(''))
    return 0


# .??..??...?##. 1,1,3
def process_spring_view(spring_view: str, arrangement: list[int]):
    # find the groups with known springs
    groups_with_known_springs = [_ for _ in re.finditer('([?#]*#+[?#]*)', spring_view)]
    contiguous_group_matches = [_ for _ in re.finditer('([#?])+', spring_view)]
    contiguous_group_arrangement_index_dict = get_contiguous_group_arrangement_index_dict(spring_view, arrangement, contiguous_group_matches)


    keep_group_index_remove_value_dict = {}
    for contiguous_group_index, possible_arrangement_indices in contiguous_group_arrangement_index_dict.items():
        # '???...???...###....???' 1,1,3
        # if a group has only one possible index, remove it from the others, also only keep the first possibility
        if len(possible_arrangement_indices) == 1:
            keep_group_index_remove_value_dict[contiguous_group_index] = possible_arrangement_indices[0]

    for keep_index, remove_value in keep_group_index_remove_value_dict.items():
        for contiguous_group_index, possible_arrangement_indices in contiguous_group_arrangement_index_dict.items():
            if contiguous_group_index == keep_index:
                continue
            elif remove_value in possible_arrangement_indices:
                possible_arrangement_indices.remove(remove_value)

    console.print(contiguous_group_arrangement_index_dict)
    # if a group has only one possible index, no previous indexes can come before it

    return 0

    # how to handle scenario where certain blocks must be in a certain position, 3 could be before, but must come at the end
    # '...???????????###????' 1,3


def get_contiguous_group_arrangement_index_dict(spring_view: str, arrangement: list[int], contiguous_group_matches: list[re.Match]):
    # check which groups could contain which part of the arrangement
    contiguous_group_arrangement_index_dict = {}
    for index, contiguous_group_match in enumerate(contiguous_group_matches):
        group_view = contiguous_group_match.group(0)
        group_max_size = len(group_view)

        # find all know spring groups within a single group
        known_springs_in_group = [_ for _ in re.finditer('#+', group_view)]

        group_min_size = 1
        if known_springs_in_group:
            group_min_size = min([len(known_spring_in_group.group(0)) for known_spring_in_group in known_springs_in_group])

        contiguous_group_arrangement_index_dict[index] = []
        for arrangement_index, spring_group_len in enumerate(arrangement):
            # check if a group could contain a spring_group
            if group_min_size <= spring_group_len <= group_max_size:
                contiguous_group_arrangement_index_dict[index].append(arrangement_index)
    return contiguous_group_arrangement_index_dict


def can_place(length_to_place: int, rest_of_spring_view: str):
    spaces_needed = length_to_place - 1

    if not fits_in_group(length_to_place, rest_of_spring_view):
        return False

    if length_to_place < get_min_group_size(rest_of_spring_view):
        return False

    if len(rest_of_spring_view) < spaces_needed:
        return False

    # check if the character at the end would not increase the groupsize
    char_at_end = rest_of_spring_view[spaces_needed - 1]
    if char_at_end == '#':
        return False

    return True


def get_min_group_size(rest_of_spring_view: str) -> int:
    size = 1
    for char in rest_of_spring_view:
        if char == '.' or char == '?':
            return size
        else:
            size += 1
    return size


def fits_in_group(length_to_place: int, rest_of_spring_view: str) -> bool:
    return length_to_place <= get_group_size(rest_of_spring_view)


def get_group_size(rest_of_spring_view: str) -> int:
    length = 1
    for char in rest_of_spring_view:
        if char == '.':
            return length
        else:
            length += 1
    return length


def split_spring_view_from_arrangements(file: list[str]):
    wells_views = []
    arrangements = []
    for line in file:
        wells_view, arrangement = line.split(' ')
        arrangements.append([int(num) for num in arrangement.split(',')])
        # wells_views.append(wells_view.replace('#', '1').replace('?', '0'))
        wells_views.append(wells_view)
    return wells_views, arrangements


def temp(arrangement, spring_view):
    length_to_place = arrangement.pop()
    for index, position_char in enumerate(spring_view):
        if position_char == '?':
            rest_of_spring_view = spring_view[index + 1:]
            if can_place(length_to_place, rest_of_spring_view):
                if arrangement and rest_of_spring_view:
                    process_spring_view(rest_of_spring_view, arrangement)
        # if a # is hit, it MUST be placed
        elif position_char == '#':
            rest_of_spring_view = spring_view[index + 1:]
            if can_place(length_to_place, rest_of_spring_view):
                if arrangement and rest_of_spring_view:
                    process_spring_view(rest_of_spring_view, arrangement)
            break


@time_function()
def run_b(file: list[str]):
    return 0


if __name__ == '__main__':
    answer_a = run_a(test_file)
    answer_b = run_b(test_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
