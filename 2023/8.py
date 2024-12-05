from util import console, parse_file_as_list, time_function
from itertools import cycle
import re
from math import lcm

test_file = parse_file_as_list('input/8_test.txt')
day_file = parse_file_as_list('input/8.txt')


@time_function()
def run_a(file: list[str]):
    instructions = cycle([0 if char == 'L' else 1 for char in file[0]])
    node_destination_dict = {match.group(1): (match.group(2), match.group(3)) for match in
                             [re.match('([A-Z0-9]{3}) = \\(([A-Z0-9]{3}), ([A-Z0-9]{3})', line) for line in file[2:]]}

    location = 'AAA'
    steps = 0
    while location != 'ZZZ':
        steps += 1
        direction = next(instructions)
        location = node_destination_dict[location][direction]
    return steps


@time_function()
def run_b(file: list[str]):
    node_destination_dict = {match.group(1): (match.group(2), match.group(3)) for match in
                             [re.match('([A-Z0-9]{3}) = \\(([A-Z0-9]{3}), ([A-Z0-9]{3})', line) for line in file[2:]]}

    starting_nodes = {node for node in node_destination_dict if node[2] == 'A'}
    end_nodes = {node for node in node_destination_dict if node[2] == 'Z'}

    node_steps = []
    for node in starting_nodes:
        instructions = cycle([0 if char == 'L' else 1 for char in file[0]])
        steps = 0
        while node not in end_nodes:
            steps += 1
            direction = next(instructions)
            node = node_destination_dict[node][direction]
        node_steps.append(steps)

    return lcm(*node_steps)


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
