from util import console, parse_file_as_list, time_function
from itertools import combinations

test_file = parse_file_as_list('input/24_test.txt')
day_file = parse_file_as_list('input/24.txt')


@time_function()
def run_a(file: list[str]):
    hailstone_with_velocities = get_hailstone_with_velocities_from_file(file)

    test_area_range = 2e14, 4e14
    intersections_in_test_area = 0
    for hailstone_a, hailstone_b in combinations(hailstone_with_velocities, 2):
        hailstone_func_a = get_hailstone_y_for_x_function(hailstone_a)
        hailstone_func_b = get_hailstone_y_for_x_function(hailstone_b)
        intersection_x_value = get_intersection_x_value(hailstone_func_a, hailstone_func_b)

        a_ok = intersects_in_test_area(intersection_x_value, test_area_range, hailstone_func_a, hailstone_a)
        b_ok = intersects_in_test_area(intersection_x_value, test_area_range, hailstone_func_b, hailstone_b)
        if a_ok and b_ok:
            intersections_in_test_area += 1

    return intersections_in_test_area


@time_function()
def run_b(file: list[str]):
    hailstone_with_velocities = get_hailstone_with_velocities_from_file(file)

    all_hailstone_functions = [get_hailstone_y_for_x_function(hailstone) for hailstone in hailstone_with_velocities]

    # console.print(all_hailstone_functions)
    rules = dict()
    x_s = []
    y_s = []
    z_s = []
    for hailstone in hailstone_with_velocities:
        (x, x_mul), (y, y_mul), (z, z_mul) = hailstone
        x_s.append((x, x_mul))
        y_s.append((y, y_mul))
        z_s.append((z, z_mul))
        console.print(all_hailstone_functions.pop())
        # console.print(f'y_mul > {y_mul} until y == {y} then x_mul < {y_mul}')
        # console.print(f'z_mul > {z_mul} until z == {z} then x_mul < {z_mul}')

    console.print('UND SO:')
    console.print(f'x under {min(x_s)[0]} with speed at least {min(x_s, key=lambda k: k[1])[1]} or x over {max(x_s)[0]} and speed no more than {max(x_s, key=lambda k: k[1])[1]}')
    console.print(f'y under {min(y_s)[0]} with speed at least {min(y_s, key=lambda k: k[1])[1]} or y over {max(y_s)[0]} and speed no more than {max(y_s, key=lambda k: k[1])[1]}')
    console.print(f'z under {min(z_s)[0]} with speed at least {min(z_s, key=lambda k: k[1])[1]} or z over {max(z_s)[0]} and speed no more than {max(z_s, key=lambda k: k[1])[1]}')



    # hailstones will collide when x, y, z are the same
    # lines need to have at least 2 convex vectors with the third being parallel, most will be 3 convex vectors

def intersects_in_test_area(x_value: float, test_area_range: tuple, hailstone_func: tuple, hailstone):
    (x, x_mul), (y, y_mul), (z, z_mul) = hailstone
    min_value, max_value = test_area_range
    x_multiplier, y_offset = hailstone_func
    y_value = ((x_value * x_multiplier) + y_offset)

    x_in_range = min_value <= x_value <= max_value
    y_in_range = min_value <= y_value <= max_value
    x_in_future = x_value <= x if (x_mul < 0) else x_value >= x

    return x_in_range and y_in_range and x_in_future


def get_intersection_x_value(hailstone_func_a: tuple, hailstone_func_b:  tuple):
    x_multiplier_a, y_offset_a = hailstone_func_a
    x_multiplier_b, y_offset_b = hailstone_func_b

    if x_multiplier_a - x_multiplier_b == 0:
        return False
    else:
        return (y_offset_b - y_offset_a) / (x_multiplier_a - x_multiplier_b)


# y = (y_step_mod / x_step_mod) * x + (current_y - (y_step_mod * (current_x / x_step_mod))
def get_hailstone_y_for_x_function(hailstone: list[tuple]):
    (x, x_mul), (y, y_mul), (z, z_mul) = hailstone

    x_multiplier = (y_mul / x_mul)
    y_offset = y - (y_mul * (x / x_mul))

    return x_multiplier, y_offset


def get_hailstone_with_velocities_from_file(file:list[str]):
    prepped_lines = [[splitline.split(', ') for splitline in line.split(' @ ')] for line in file]
    hailstone_with_velocities = [[(int(coord), int(velocity)) for coord, velocity in zip(coordinates, velocities)] for coordinates, velocities in prepped_lines]
    return hailstone_with_velocities


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(test_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
