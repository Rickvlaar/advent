from util import console, parse_file_as_list, time_function

test_file = parse_file_as_list('input/{day_no}_test.txt')
day_file = parse_file_as_list('input/{day_no}.txt')


@time_function()
def run_a(file: list[str]):
    pass


@time_function()
def run_b(file: list[str]):
    pass


if __name__ == '__main__':
    answer_a = run_a(test_file)
    answer_b = run_b(test_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
