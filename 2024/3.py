from util import console, parse_file_as_list, time_function
import re

test_file = parse_file_as_list('input/3_test.txt')
day_file = parse_file_as_list('input/3.txt')


@time_function()
def run_a(file: list[str]):
    # fixme: there seem to be line endings within the real day input string
    matcher = re.compile(pattern='mul\\((\\d*),(\\d*)\\)')
    total = 0
    for line in file:
        for multiply_command_match in matcher.finditer(line):
            total += int(multiply_command_match.group(1)) * int(multiply_command_match.group(2))
    return total


@time_function()
def run_b(file: list[str]):
    pass


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(test_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
