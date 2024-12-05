from util import console, parse_file_as_list, time_function

test_file = parse_file_as_list('input/1b_test.txt')
day_file = parse_file_as_list('input/1.txt')

letter_digits = {
        'one':   '1',
        'two':   '2',
        'three': '3',
        'four':  '4',
        'five':  '5',
        'six':   '6',
        'seven': '7',
        'eight': '8',
        'nine':  '9'
}


@time_function(100)
def run_a(file: list[str]):
    vals = []
    for line in file:
        char_str = ''
        for char in line:
            if char.isnumeric():
                char_str += char
                break
        for char in reversed(line):
            if char.isnumeric():
                char_str += char
                break
        vals.append(int(char_str))

    return sum(vals)


@time_function(100)
def run_b(file: list[str]):
    vals = []

    for line in file:
        char_str = ''

        index_letter_dict = {}
        for letter_dig, dig in letter_digits.items():
            min_index = line.find(letter_dig)
            max_index = line.rfind(letter_dig)

            if min_index != -1:
                index_letter_dict[min_index] = dig
            if max_index != -1:
                index_letter_dict[max_index] = dig

        lowest_index = min(index_letter_dict) if index_letter_dict else 999
        for index, char in enumerate(line):
            if index >= lowest_index:
                char_str += index_letter_dict[lowest_index]
                break
            elif char.isnumeric():
                char_str += char
                break
        highest_index = max(index_letter_dict) if index_letter_dict else -1
        for index, char in enumerate(reversed(line)):
            if highest_index > len(line) - 1 - index:
                char_str += index_letter_dict[highest_index]
                break
            elif char.isnumeric():
                char_str += char
                break
        vals.append(int(char_str))
    return sum(vals)


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
