from util import console, parse_file_as_list, time_function
from math import prod

test_file = parse_file_as_list('input/2_test.txt')
day_file = parse_file_as_list('input/2.txt')


@time_function()
def run_a(file: list[str]):
    max_cubes_config = {'blue':  14,
                        'green': 13,
                        'red':   12}

    game_details_dict = parse_game_strings(file)
    possible_games = get_possible_game_numbers(game_details_dict, max_cubes_config)
    return sum(possible_games)


@time_function()
def run_b(file: list[str]):
    game_details_dict = parse_game_strings(file)
    needed_cube_colours = get_needed_cubes_by_colour(game_details_dict)
    powers = [prod(details.values()) for details in needed_cube_colours.values()]
    return sum(powers)


def parse_game_strings(games_strings: list[str]):
    game_dict = {}
    for game in games_strings:
        game_name, splitter, game_details = game.partition(':')
        game_no = int(game_name.lstrip('Game '))
        game_details = [{colour: int(count) for count, colour in [cubes.strip().split(' ') for cubes in turn.split(',')]} for turn in game_details.split('; ')]
        game_dict[game_no] = game_details
    return game_dict


def get_possible_game_numbers(games: dict[int: list[dict[str: int]]], max_cubes_config: dict[str: int]):
    possible_games = []
    for game_no, game_details in games.items():
        if is_game_possible(game_details, max_cubes_config):
            possible_games.append(game_no)
    return possible_games


def is_game_possible(game_details, max_cubes_config):
    for turn in game_details:
        for colour in turn:
            if turn[colour] > max_cubes_config[colour]:
                return False
    return True


def get_needed_cubes_by_colour(game_details: dict[int: list[dict[str: int]]]):
    needed_cube_colours = {}
    for game_no, details in game_details.items():
        needed_cube_colours[game_no] = {'blue':  0,
                                        'green': 0,
                                        'red':   0}
        for turn in details:
            for cube_colour, amount in turn.items():
                if amount > needed_cube_colours[game_no][cube_colour]:
                    needed_cube_colours[game_no][cube_colour] = amount

    return needed_cube_colours


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
