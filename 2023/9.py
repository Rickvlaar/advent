from util import console, parse_file_as_list, time_function
from itertools import pairwise

test_file = parse_file_as_list('input/9_test.txt')
day_file = parse_file_as_list('input/9.txt')


@time_function()
def run_a(file: list[str]):
    expanded_histories = expand_histories(file)

    answers = []
    for result in expanded_histories:
        num_to_add = 0
        for sub_result in reversed(result):
            num_to_add = sub_result[-1] + num_to_add
            sub_result.append(num_to_add)
        answers.append(result[0][-1])

    return sum(answers)


@time_function()
def run_b(file: list[str]):
    expanded_histories = expand_histories(file)

    answers = []
    for result in expanded_histories:
        num_to_add = 0
        for sub_result in reversed(result):
            num_to_add = sub_result[0] - num_to_add
            sub_result.insert(0, num_to_add)
        answers.append(result[0][0])

    return sum(answers)


def expand_histories(history: list[str]):
    inted_list = [[int(char) for char in line.split(' ')] for line in history]

    get_num_difference = lambda a, b: b - a
    all_int_list_results = []
    for int_list in inted_list:
        results = [int_list]
        sub_result = int_list
        while True:
            sub_result = [get_num_difference(pair[0], pair[1]) for pair in pairwise(sub_result)]
            results.append(sub_result)
            if not any(sub_result):
                break
        all_int_list_results.append(results)
    return all_int_list_results


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
