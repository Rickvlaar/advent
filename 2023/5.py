from util import console, parse_file_as_list, time_function
import re

test_file = parse_file_as_list('input/5_test.txt')
day_file = parse_file_as_list('input/5.txt')


@time_function()
def run_a(file):
    seeds = [int(seed_no) for seed_no in file[0].split('seeds: ')[1].split(' ')]
    bal_dict = parse_file(file)
    locations = determine_locations(seeds, bal_dict)
    return min(locations)


@time_function()
def run_b(file):
    seed_range_pairs = [int(seed_no) for seed_no in file[0].split('seeds: ')[1].split(' ')]
    seed_ranges = [(seed_range_start, seed_range_start + range_len - 1) for seed_range_start, range_len in zip(seed_range_pairs[::2], seed_range_pairs[1::2])]
    source_to_target_mappings = parse_file(file)
    locations = determine_locations_by_range(seed_ranges, source_to_target_mappings)
    return min(locations)[0]


def parse_file(file: list[str]):
    pattern = '([a-z]*)-to-([a-z]*)'
    source_to_target_mappings = {}
    for index, line in enumerate(file):
        if 'map' in line:
            source_target = re.match(pattern, line).groups()
            source_to_target_mappings[source_target] = create_source_dest_map(file=file, start_index=index + 1)
        else:
            continue
    return source_to_target_mappings


def determine_locations(seeds: list[int], bal_dict: dict[tuple: list[list:int]]):
    # destination_start, source_start, range_len
    locations = []
    for seed_no in seeds:
        for ranges in bal_dict.values():
            for seed_range in ranges:
                source_range_start = seed_range[1]
                source_range_end = source_range_start + seed_range[2] - 1
                if source_range_start <= seed_no <= source_range_end:
                    diff = seed_no - source_range_start
                    destination_range_start = seed_range[0]
                    seed_no = destination_range_start + diff
                    break
        locations.append(seed_no)
    return locations


# Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82

def determine_locations_by_range(seeds_ranges: list[tuple], source_to_target_mappings: dict[tuple: list[list:int]]):
    # destination_start, source_start, range_len
    for ranges in source_to_target_mappings.values():
        new_ranges = []
        for seed_range in seeds_ranges:
            changes = False
            for mapped_range in ranges:

                source_range_start = mapped_range[1]
                source_range_end = source_range_start + mapped_range[2] - 1

                destination_range_start = mapped_range[0]
                destination_range_end = destination_range_start + mapped_range[2] - 1

                # fully in target range: replace source range
                if source_range_start <= seed_range[0] and seed_range[1] <= source_range_end:
                    diff = seed_range[0] - source_range_start
                    diff_end = seed_range[1] - seed_range[0]
                    new_range = destination_range_start + diff, destination_range_start + diff + diff_end
                    new_ranges.append(new_range)
                    changes = True
                    break
                # fully envelops target range: split in three ranges
                elif seed_range[0] <= source_range_start and seed_range[1] >= source_range_end:
                    split_range_left = (seed_range[0], source_range_start - 1)
                    split_range_right = (source_range_end + 1, seed_range[1])
                    seeds_ranges.append(split_range_left)
                    seeds_ranges.append(split_range_right)
                    new_range = destination_range_start, destination_range_end
                    new_ranges.append(new_range)
                    changes = True
                # right split range: two ranges
                elif source_range_start <= seed_range[0] <= source_range_end:
                    split_range_right = (source_range_end + 1, seed_range[1])
                    seeds_ranges.append(split_range_right)
                    diff = seed_range[0] - source_range_start
                    new_range = destination_range_start + diff, destination_range_end
                    new_ranges.append(new_range)
                    changes = True
                # left split range : two ranges
                elif source_range_start <= seed_range[1] <= source_range_end:
                    split_range_left = (seed_range[0], source_range_start - 1)
                    seeds_ranges.append(split_range_left)
                    diff = source_range_end - seed_range[1]
                    new_range = destination_range_start, destination_range_end - diff
                    new_ranges.append(new_range)
                    changes = True
            if not changes:
                new_ranges.append(seed_range)
        seeds_ranges = new_ranges
    return seeds_ranges


def create_source_dest_map(file: list[str], start_index: int):
    seed_nos = []
    for line in file[start_index:]:
        if line == '':
            return seed_nos
        seed_nos.append([int(seed_no) for seed_no in line.split(' ')])
    return seed_nos


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
