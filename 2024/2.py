from util import console, parse_file_as_list, time_function
from itertools import pairwise

test_file = parse_file_as_list('input/2_test.txt')
day_file = parse_file_as_list('input/2.txt')


@time_function()
def run_a(file: list[str]):
    reports = [[int(val) for val in line.split(' ')] for line in file]
    safe_count = 0
    for report in reports:
        if is_safe_report(report):
            safe_count += 1

    return safe_count


@time_function()
def run_b(file: list[str]):
    reports = [[int(val) for val in line.split(' ')] for line in file]
    safe_count = 0
    for report in reports:
        if is_safe_report(report):
            safe_count += 1

    return safe_count


def is_safe_report(report: list[int]) -> bool:
    initial_direction_increasing = report[0] < report[1]

    for left_value, right_value in pairwise(report):
        # determine if direction is stable
        direction_increasing = left_value < right_value
        if initial_direction_increasing != direction_increasing:
            return False

        # determine if values are within 1 to 3
        difference = abs(left_value - right_value)
        if difference > 3 or difference < 1:
            return False


    return True


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(test_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
