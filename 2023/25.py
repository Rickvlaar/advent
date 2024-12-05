from util import console, parse_file_as_list, time_function
from itertools import combinations
from collections import defaultdict

test_file = parse_file_as_list('input/25_test.txt')
day_file = parse_file_as_list('input/25.txt')


@time_function()
def run_a(file: list[str]):
    component_connections_dict = parse_input(file)





    console.print(component_connections_dict)

    pass


@time_function()
def run_b(file: list[str]):
    pass


def parse_input(file: list[str]):
    component_connections_dict = defaultdict(set)
    for line in file:
        prefix, values_string = line.split(':')
        values = values_string[1:].split(' ')

        for value in values:
            component_connections_dict[prefix].add(value)
            component_connections_dict[value].add(prefix)

    return component_connections_dict



if __name__ == '__main__':
    answer_a = run_a(test_file)
    answer_b = run_b(test_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
