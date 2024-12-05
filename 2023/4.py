from util import console, parse_file_as_list, time_function

test_file = parse_file_as_list('input/4_test.txt')
day_file = parse_file_as_list('input/4.txt')


@time_function()
def run_a(file: list[str]):
    points_per_game = []

    for game in file:
        won_numbers = get_won_numbers(game)

        points = 0
        for x in range(len(won_numbers)):
            points = 2 * points if points else 1

        points_per_game.append(points)
    return sum(points_per_game)


@time_function()
def run_b(file: list[str]):
    max_card_no = len(file)
    how_many_copies = [1 for _ in file]

    for index, game in enumerate(file):
        won_numbers = get_won_numbers(game)

        for index_adjust in range(len(won_numbers)):

            if index + index_adjust + 1 == max_card_no:
                break

            how_many_copies[index + index_adjust + 1] += how_many_copies[index]

    return sum(how_many_copies)


def get_won_numbers(game: str) -> set[int]:
    card_winning_nums, your_numbers = game.split('| ')
    your_numbers = {int(num.strip()) for num in your_numbers.strip().split(' ') if num.isnumeric()}
    card, winning_numbers = card_winning_nums.split(': ')
    winning_numbers = {int(num.strip()) for num in winning_numbers.strip().split(' ') if num.isnumeric()}
    return winning_numbers.intersection(your_numbers)


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
