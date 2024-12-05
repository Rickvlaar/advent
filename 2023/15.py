import re

from util import console, parse_file_as_list, time_function
from collections import OrderedDict

test_file = parse_file_as_list('input/15_test.txt')
day_file = parse_file_as_list('input/15.txt')


@time_function()
def run_a(file: list[str]):
    return sum([get_hashed_value(value) for value in file[0].split(',')])


@time_function()
def run_b(file: list[str]):
    instruction_tuples = convert_file_to_instructions(file[0])
    boxes_dict = fill_lens_boxes(instruction_tuples)
    return sum(calculate_focal_strengths(boxes_dict))


def fill_lens_boxes(instruction_tuples: list[tuple]):
    boxes_dict = {num: OrderedDict() for num in range(256)}

    for instruction, operator, lens_value in instruction_tuples:
        box_number = get_hashed_value(instruction)
        if operator == '-':
            if instruction in boxes_dict[box_number]:
                boxes_dict[box_number].pop(instruction)
        else:
            boxes_dict[box_number][instruction] = int(lens_value)

    return boxes_dict


def calculate_focal_strengths(boxes_dict: dict[int: OrderedDict]):
    focal_strengths = []
    for box_number, box in boxes_dict.items():
        if not box:
            continue
        for slot_no, focal_strength in enumerate(box.values()):
            focal_strengths.append((box_number + 1) * (slot_no + 1) * focal_strength)
    return focal_strengths


def get_hashed_value(string_to_hash: str) -> int:
    current_value = 0
    for letter in string_to_hash:
        ascii_val = ord(letter)
        current_value += ascii_val
        current_value *= 17
        current_value %= 256
    return current_value


def convert_file_to_instructions(line: str):
    letter_vals = [split_line for split_line in line.split(',')]
    pattern = re.compile('([a-zA-Z]+)([=-])([0-9]*)')
    instruction_tuples = []
    for val in letter_vals:
        matched = pattern.match(string=val)
        instruction = (matched.group(1), matched.group(2), matched.group(3))
        instruction_tuples.append(instruction)
    return instruction_tuples


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
