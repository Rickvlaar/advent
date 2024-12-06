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
    single_string_memory = ''.join(file)
    multiply_command_matcher = re.compile(pattern='mul\\((\\d*),(\\d*)\\)')
    enablement_command_matcher = re.compile(pattern='(do\\(\\))|(don\'t\\(\\))')

    enablement_pos_dict = {}
    for enablement_command in enablement_command_matcher.finditer(single_string_memory):
        enablement_pos_dict[enablement_command.end()] = True if enablement_command[0] == 'do()' else False

    enablement_command_posses = sorted(enablement_pos_dict, reverse=True)
    enable_multiplication = True
    total = 0
    for multiply_command in multiply_command_matcher.finditer(single_string_memory):
        start_index = multiply_command.start()
        for pos in enablement_command_posses:
            if pos <= start_index:
                enable_multiplication = enablement_pos_dict[pos]
                break

        if enable_multiplication:
            total += int(multiply_command.group(1)) * int(multiply_command.group(2))

    return total


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
