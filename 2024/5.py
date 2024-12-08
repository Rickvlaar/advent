from util import console, parse_file_as_list, time_function
from collections import defaultdict

test_file = parse_file_as_list('input/5_test.txt')
day_file = parse_file_as_list('input/5.txt')


@time_function()
def run_a(file: list[str]):
    ordering_rules, print_instructions = parse_file(file)

    valid_pages_sum = 0
    for print_instruction in print_instructions:
        if validate_print_instruction(print_instruction, ordering_rules):
            middle_value_index = int((len(print_instruction) / 2) - 0.5)
            valid_pages_sum += print_instruction[middle_value_index]
    return valid_pages_sum


@time_function()
def run_b(file: list[str]):
    ordering_rules, print_instructions = parse_file(file)


    pass


def validate_print_instruction(print_instruction: list[int], ordering_rules: dict[int, list[int]]) -> bool:
    for index, page_no in enumerate(print_instruction):
        print_before_pages = ordering_rules[page_no]
        for page in print_instruction[:index]:
            if page in print_before_pages:
                return False
    return True


def parse_file(file: list[str]):
    for index, line in enumerate(file):
        if line == '':
            ordering_rules_raw = [[int(val) for val in line.split('|')] for line in file[:index]]
            ordering_rules = defaultdict(list[int])
            for rule in ordering_rules_raw:
                ordering_rules[rule[0]].append(rule[1])

            print_instructions = [[int(val) for val in line.split(',')] for line in file[index + 1:]]
            return ordering_rules, print_instructions


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(test_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
