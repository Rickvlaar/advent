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
        if is_safe_report(report, True):
            safe_count += 1

    return safe_count


def is_safe_report(report: list[int], tolerate_error: bool = False) -> bool:
    initial_direction_increasing = report[0] < report[1]

    for index, left_value in enumerate(report):
        if index + 1 == len(report):
            return True

        right_value = report[index + 1]

        # determine if direction is stable or difference outside of limit
        direction_unstable = (left_value < right_value) != initial_direction_increasing
        difference_above_limit = abs(left_value - right_value) > 3 or abs(left_value - right_value) < 1

        if direction_unstable or difference_above_limit:
            if tolerate_error:
                if direction_unstable and index == 1:
                    is_safe_without_first = is_safe_report(report[1:])
                    if is_safe_without_first:
                        return True
                # remove left first
                report_copy = report.copy()
                del report_copy[index]
                is_safe_without_left = is_safe_report(report_copy)
                if is_safe_without_left:
                    return True
                else:
                    del report[index + 1]
                    return is_safe_report(report)
            else:
                return False


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file) #311 is too low, 320 wrong

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
