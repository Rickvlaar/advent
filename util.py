from typing import Callable
from itertools import product
from rich.console import Console
import time
import numpy as np

console = Console(color_system='truecolor', width=250)


def parse_file_as_list(file):
    return [num.rstrip('\n') for num in open(file=file, newline='\n')]


def convert_str_list_to_int_list(str_list: list[str]) -> list[int]:
    return [int(element) for element in str_list]


# Time function runtime in ms
def get_runtime(function: Callable):
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        result = function(*args, **kwargs)
        end = time.perf_counter_ns()
        console.print(f'[bold blue]{function.__name__}[/bold blue]',
                      '[red]ran for[/red]', (end - start) / 1e6,
                      '[red]ms[/red]')
        return result

    return wrapper


# Time function runtime for 'n' iterations in ms
def time_function(iterations: int = 1):
    def decorator(function: Callable):
        def wrapper(*args, **kwargs):
            start = time.perf_counter_ns()

            result = None
            for _ in range(iterations):
                result = function(*args, **kwargs)

            end = time.perf_counter_ns()

            # Average runtime
            console.print(f'[bold blue]{function.__name__}[/bold blue]',
                          f'[bright_magenta bold]AVERAGE[/bright_magenta bold]',
                          f'[red]runtime for[/red]',
                          f'{iterations}',
                          f'[red]iterations[/red]',
                          (end - start) / 1e6 / iterations,
                          '[red]ms[/red]')

            return result

        return wrapper

    return decorator


def get_the_hood_8(grid: np.array, ignored_values: set[str | int | bool] = None):
    max_y = grid.shape[0]
    max_x = grid.shape[1]
    the_hood = dict()
    for y, line in enumerate(grid):
        for x, value in enumerate(line):
            if ignored_values and value in ignored_values:
                continue
            xs = [x_2 for x_2 in range(x - 1, x + 2) if 0 <= x_2 < max_x]
            ys = [y_2 for y_2 in range(y - 1, y + 2) if 0 <= y_2 < max_y]
            the_hood[(y, x)] = [coord for coord in product(ys, xs) if coord != (y, x)]
    return the_hood


def get_the_hood_straight(grid: np.array, ignored_values: set[str | int | bool] = None) -> dict[tuple: list[tuple]]:
    max_y = grid.shape[0] - 1
    max_x = grid.shape[1] - 1
    the_hood = dict()
    for y, line in enumerate(grid):
        for x, value in enumerate(line):
            if ignored_values and value in ignored_values:
                continue
            neighbs = []
            if x > 0:
                if ignored_values and grid[y, x - 1] not in ignored_values:
                    neighbs.append((y, x - 1))
            if x < max_x:
                if ignored_values and grid[y, x + 1] not in ignored_values:
                    neighbs.append((y, x + 1))
            if y > 0:
                if ignored_values and grid[y - 1, x] not in ignored_values:
                    neighbs.append((y - 1, x))
            if y < max_y:
                if ignored_values and grid[y + 1, x] not in ignored_values:
                    neighbs.append((y + 1, x))
            the_hood[(y, x)] = neighbs
    return the_hood


# insert coordinates with y, x arrangement
def calc_manhattan_dist(coord_1: tuple, coord_2: tuple):
    x_dist = abs(coord_1[1] - coord_2[1])
    y_dist = abs(coord_1[0] - coord_2[0])
    manhattan_distance = x_dist + y_dist
    return manhattan_distance
