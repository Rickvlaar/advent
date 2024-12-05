from util import console, parse_file_as_list, time_function
from collections import Counter

test_file = parse_file_as_list('input/1_test.txt')
day_file = parse_file_as_list('input/1.txt')


@time_function()
def run_a(file: list[str]):
    left_list, right_list = get_two_lists(file)

    left_list.sort()
    right_list.sort()

    difference = 0
    for index, left_value in enumerate(left_list):
        difference += abs(left_value - right_list[index])

    return difference


@time_function()
def run_b(file: list[str]):
    left_list, right_list = get_two_lists(file)

    counted_right_list = Counter(right_list)
    similarity_score = 0
    for left_value in left_list:
        time_in_right_list_count = counted_right_list.get(left_value)
        similarity_score += time_in_right_list_count * left_value if time_in_right_list_count is not None else 0

    return similarity_score



def get_two_lists(file: list[str]):
    split_values_list = [line.split('   ') for line in file]
    left_list = list()
    right_list = list()
    for left, right in split_values_list:
        left_list.append(int(left))
        right_list.append(int(right))

    return left_list, right_list


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
