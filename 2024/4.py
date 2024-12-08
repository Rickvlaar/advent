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
    pass


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(test_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
