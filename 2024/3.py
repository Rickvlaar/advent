from util import console, parse_file_as_list, time_function
import re

test_file = parse_file_as_list('input/3_test.txt')
day_file = parse_file_as_list('input/3.txt')


@time_function()
def run_a(file: list[str]):
    # There are line endings within the real day input string, so make it a single line
    single_string_memory = ''.join(file)
    matcher = re.compile(pattern='mul\\((\\d*),(\\d*)\\)')
    total = sum([int(multiply_command_match.group(1)) * int(multiply_command_match.group(2)) for multiply_command_match in matcher.finditer(single_string_memory)])
    return total


@time_function()
def run_b(file: list[str]):
    pass


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(test_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
