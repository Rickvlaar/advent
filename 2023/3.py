from util import console, parse_file_as_list, time_function, get_the_hood_8
import numpy as np
import re
from string import punctuation
from collections import defaultdict
from math import prod

test_file = parse_file_as_list('input/3_test.txt')
day_file = parse_file_as_list('input/3.txt')


@time_function()
def run_a(file):
    valid_engine_symbols = set(punctuation)
    valid_engine_symbols.remove('.')

    y_numbers_dict = find_numbers(file)
    engine = np.array([list(line) for line in file])
    the_hood = get_the_hood_8(engine, ignored_values={'.'})

    engine_part_numbers = []
    for y, number_matches in y_numbers_dict.items():
        # skip emtpy values
        if not number_matches:
            continue

        for match in number_matches:
            valid_number = check_engine_number(y, match, engine, valid_engine_symbols, the_hood)
            if valid_number:
                engine_part_numbers.append(valid_number)

    return sum(engine_part_numbers)


@time_function()
def run_b(file):
    y_numbers_dict = find_numbers(file)
    engine = np.array([list(line) for line in file])
    the_hood = get_the_hood_8(engine, ignored_values={'.'})

    gear_coord_numbers_dict = defaultdict(list)
    for y, number_matches in y_numbers_dict.items():
        # skip emtpy values
        if not number_matches:
            continue

        for match in number_matches:
            result = check_engine_gear(y, match, engine, the_hood)
            if result:
                gear_coord_numbers_dict[result[0]].append(result[1])

    gear_ratios = []
    for gear_coord, engine_numbers in gear_coord_numbers_dict.items():
        if len(engine_numbers) == 2:
            gear_ratios.append(prod(engine_numbers))

    return sum(gear_ratios)


def check_engine_gear(y, match, engine, the_hood):
    for x in range(match.span()[0], match.span()[1]):
        for coord_value in the_hood[y, x]:
            symbol = engine[coord_value]
            if symbol == '*':
                return coord_value, int(match.group(0))


def check_engine_number(y, match, engine, valid_engine_symbols, the_hood):
    for x in range(match.span()[0], match.span()[1]):
        for coord_value in the_hood[y, x]:
            symbol = engine[coord_value]
            if symbol in valid_engine_symbols:
                return int(match.group(0))


def find_numbers(file):
    pattern = re.compile('([0-9])+')
    y_numbers_dict = {index: [match for match in pattern.finditer(line)] for index, line in enumerate(file)}
    return y_numbers_dict


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
