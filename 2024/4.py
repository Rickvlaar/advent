from sympy.logic.boolalg import Boolean

from util import console, parse_file_as_list, time_function, convert_str_list_to_int_list
import numpy as np
import re

test_file = parse_file_as_list('input/4_test.txt')
day_file = parse_file_as_list('input/4.txt')


@time_function()
def run_a(file: list[str]):
    xmas_map = np.array(file)

    counter = 0

    # horizontals first
    for line in xmas_map:
        counter += sum([1 for found_xmas in re.finditer(pattern='XMAS', string=line)])
        counter += sum([1 for found_xmas in re.finditer(pattern='XMAS', string=line[::-1])])

    # verticals
    xmas_map = np.array([list(line) for line in file])
    for column_no in range(len(xmas_map)):
        column = ''.join(xmas_map[:, column_no])
        counter += sum([1 for found_xmas in re.finditer(pattern='XMAS', string=column)])
        counter += sum([1 for found_xmas in re.finditer(pattern='XMAS', string=column[::-1])])

    # diagonals
    for diagonal_no in range(-len(xmas_map) + 1, len(xmas_map)):
        diagonal = ''.join(np.diag(xmas_map, k=diagonal_no))
        counter += sum([1 for found_xmas in re.finditer(pattern='XMAS', string=diagonal)])
        counter += sum([1 for found_xmas in re.finditer(pattern='XMAS', string=diagonal[::-1])])

        flipped_xmas_map = np.fliplr(xmas_map)
        diagonal = ''.join(np.diag(flipped_xmas_map, k=diagonal_no))
        counter += sum([1 for found_xmas in re.finditer(pattern='XMAS', string=diagonal)])
        counter += sum([1 for found_xmas in re.finditer(pattern='XMAS', string=diagonal[::-1])])

    return counter


@time_function()
def run_b(file: list[str]):
    xmas_map = np.array([list(line) for line in file])

    # slice array into 3,3 blocks and see if X-MAS could be fitted in there
    counter = 0
    for y_index in range(len(xmas_map) - 2):
        for x_index in range(len(xmas_map) -2):
            three_by_three_block = xmas_map[y_index: y_index + 3, x_index: x_index + 3]
            if check_is_xmas_block(three_by_three_block):
                counter += 1
    return counter



def check_is_xmas_block(three_by_three_block: np.array) -> bool:
    # could be done efficiently with diagonals
    for _ in range(4):
        diagonal_top = ''.join(np.diag(three_by_three_block, k=0))
        flipped_up_three_by_three_block = np.flipud(three_by_three_block)
        diagonal_bottom = ''.join(np.diag(flipped_up_three_by_three_block, k=0))

        if diagonal_top == 'MAS' and diagonal_bottom == 'MAS':
            return True

        # rotate block 90 degrees
        three_by_three_block = np.rot90(three_by_three_block)
    return False


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
