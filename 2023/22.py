from util import console, parse_file_as_list, time_function
from geometry_util import Cuboid
import plotly.graph_objects as go
from dataclasses import dataclass, field

test_file = parse_file_as_list('input/22_test.txt')
day_file = parse_file_as_list('input/22.txt')


@dataclass
class Brick(Cuboid):
    id: str | int = None
    supports: list['Brick'] = field(default_factory=list)
    supported_by: list['Brick'] = field(default_factory=list)
    fell: bool = False

    def get_brick_chain_count(self, current_chain_size: int):
        if all([supporting_brick.fell for supporting_brick in self.supported_by]):
            current_chain_size += 1
            self.fell = True

            if not self.supports:
                return current_chain_size

            for brick in self.supports:
                current_chain_size = brick.get_brick_chain_count(current_chain_size)

        return current_chain_size

    def determine_brick_chain_destroy_count(self, current_chain_size: int = 0):
        if not self.supports:
            return current_chain_size

        self.fell = True

        for brick in self.supports:
            current_chain_size = brick.get_brick_chain_count(current_chain_size)

        return current_chain_size


@time_function()
def run_a(file: list[str]):
    bricks = convert_file_to_bricks(file)

    # order bricks by closest to ground
    bricks.sort(key=lambda brick: min(brick.z_range_tuple))
    bricks = drop_the_bricks(bricks)
    bricks = get_brick_supports(bricks)

    destroyables = set()
    for brick in bricks:
        if len(brick.supports) == 0:
            destroyables.add(brick.id)

        if len(brick.supported_by) == 1:
            continue
        # if supported by more than 1 brick, the supporters might be destroyable
        elif len(brick.supported_by) > 1:
            for supporting_brick in brick.supported_by:
                # if a supporting brick supports bricks which all have other supports it can be removed
                if all([len(supported_brick.supported_by) > 1 for supported_brick in supporting_brick.supports]):
                    destroyables.add(supporting_brick.id)

    # render_bricks(bricks, destroyables)
    return len(destroyables)


@time_function()
def run_b(file: list[str]):
    bricks = convert_file_to_bricks(file)

    # order bricks by closest to ground
    bricks.sort(key=lambda brick: min(brick.z_range_tuple))
    bricks = drop_the_bricks(bricks)
    bricks = get_brick_supports(bricks)

    all_chain_sizes = []
    for brick in bricks:
        all_chain_sizes.append(brick.determine_brick_chain_destroy_count(0))
        # reset the bricks
        for reset_brick in bricks:
            reset_brick.fell = False

    return sum(all_chain_sizes)


def get_brick_supports(bricks: list[Brick]):
    bricks.sort(key=lambda brick: min(brick.z_range_tuple))

    for brick_index, brick_to_destroy in enumerate(bricks):
        for compare_brick in bricks:
            if compare_brick.id == brick_to_destroy.id:
                continue

            # when x y and z touch, it supports a block
            x_overlap = brick_to_destroy.get_overlap_range(brick_to_destroy.x_range_tuple, compare_brick.x_range_tuple)
            y_overlap = brick_to_destroy.get_overlap_range(brick_to_destroy.y_range_tuple, compare_brick.y_range_tuple)

            if x_overlap and y_overlap and brick_to_destroy.z_range_tuple[1] == compare_brick.z_range_tuple[0]:
                brick_to_destroy.supports.append(compare_brick)
                compare_brick.supported_by.append(brick_to_destroy)

    return bricks


def drop_the_bricks(bricks: list[Brick]) -> list[Brick]:

    # currently sorted low to high for bottom z value
    ground_z = 0
    placed_brick = []
    for brick_index, brick_to_place in enumerate(bricks):
        # sort by highest Z value, because that brick will be hit first potentially
        placed_brick.sort(key=lambda brick: max(brick.z_range_tuple), reverse=True)
        brick_original_z_value = brick_to_place.z_range_tuple[0]
        hit_brick = False
        # drop it to the ground
        for compare_brick in placed_brick:
            # when x and y planes overlap, this block cannot pass, so place is on top
            x_overlap = brick_to_place.get_overlap_range(brick_to_place.x_range_tuple, compare_brick.x_range_tuple)
            y_overlap = brick_to_place.get_overlap_range(brick_to_place.y_range_tuple, compare_brick.y_range_tuple)

            if x_overlap and y_overlap:
                brick_to_place.z_range_tuple = (compare_brick.z_range_tuple[1],
                                                compare_brick.z_range_tuple[1] + brick_to_place.z_range_tuple[1] - brick_original_z_value)
                hit_brick = True
                break

        if not hit_brick:
            brick_to_place.z_range_tuple = (ground_z,
                                            ground_z + brick_to_place.z_range_tuple[1] - brick_original_z_value)

        placed_brick.append(brick_to_place)

    return bricks


def convert_file_to_bricks(file: list[str]) -> list[Brick]:
    block_dimensions = [[tuple(int(char) for char in coordinates.split(',')) for coordinates in line.split('~')] for
                        line in file]
    bricks = []
    brick_id = 0
    for dim_a, dim_b in block_dimensions:
        coordinate_range_tuples = [(dims[0] - 1, dims[1]) for dims in zip(dim_a, dim_b)]

        x_range, y_range, z_range = coordinate_range_tuples
        new_brick = Brick(
                id=brick_id,
                x_range_tuple=x_range,
                y_range_tuple=y_range,
                z_range_tuple=z_range
        )
        brick_id += 1
        bricks.append(new_brick)

    return bricks


def render_bricks(bricks: list[Brick], destroyables:set[str]):
    for brick in bricks:
        fill_value = 0
        if brick.id in destroyables:
            fill_value = 5
        brick.three_d(fill_value)
        brick.shape.name = brick.id

    data = [brick.shape for brick in bricks[:50]]
    fig = go.Figure(data=data)
    fig.update_layout(width=1200, height=900)
    fig.update_scenes(aspectratio={'x':1, 'y':1, 'z':1})
    fig.show()


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
