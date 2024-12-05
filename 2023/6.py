from util import console, parse_file_as_list, time_function
from sympy import symbols, solve
from math import prod, sqrt
import re

test_file = parse_file_as_list('input/6_test.txt')
day_file = parse_file_as_list('input/6.txt')


@time_function()
def run_a(file: list[str]):
    time_records_dict = get_time_records_dict(file)

    successes_per_race = []
    for time, record in time_records_dict.items():
        successes_per_race.append(determine_possible_wins(time, record))

    return prod(successes_per_race)


@time_function()
def run_b(file: list[str]):
    time = int(''.join([match.group(0) for match in re.finditer('\\d+', file[0])]))
    record = int(''.join([match.group(0) for match in re.finditer('\\d+', file[1])]))
    return determine_possible_wins_performant(time, record)


def determine_possible_wins(time: int, record: int) -> int:
    successes = 0
    for acceleration in range(time):
        distance_traveled = (time - acceleration) * acceleration
        if distance_traveled > record:
            successes += 1
    return successes


def determine_possible_wins_performant(time: int, record: int) -> int:
    acceleration = symbols('acceleration')
    expr = (time - acceleration) * acceleration - record
    solved = solve(expr, simplify=False)
    return round(solved[1]) - round(solved[0] + 1)


def get_time_records_dict(file: list[str]):
    times = [int(match.group(0)) for match in re.finditer('\\d+', file[0])]
    records = [int(match.group(0)) for match in re.finditer('\\d+', file[1])]
    time_records_dict = {time: record for time, record in zip(times, records)}
    return time_records_dict


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
